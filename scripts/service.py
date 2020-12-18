import os
import json
from cf_common import get_space_guid, cf_client_initialise, exception_handler_function


def check_service_plan_exists(client, service_plan):
    service_plan_exists = False
    for plan in client.v2.service_plans:
        if plan["entity"]["name"] == service_plan:
            service_plan_exists = True
            service_plan_guid = plan["metadata"]["guid"]

    if service_plan_exists:
        return service_plan_guid
    else:
        exception_handler_function(msg=f"Could not find service plan: {service_plan}")


def create_service_with_parameters(
    client, instance_name, service_plan_guid, space_guid, parameters, threshold=20
):
    try:
        client.v2.service_instances.create(
            space_guid=space_guid,
            instance_name=instance_name,
            plan_guid=service_plan_guid,
            accepts_incomplete=True,
            parameters=parameters,
        )
        print("Service instance creation in progress for: {}".format(instance_name))
        for i in range(threshold):
            i = i + 1
            service_created = check_service_status(
                client=client, instance_count=i, instance_name=instance_name
            )
            if service_created:
                break
            if i >= 40:
                exception_handler_function(msg=f"Timed out waiting for {instance_name} to reach desired state")
    except Exception as e:
        exception_handler_function(msg=f"Received exception when creating service instance: {instance_name}: {e}")


def create_service(client, instance_name, service_plan_guid, space_guid, threshold=20):
    try:
        client.v2.service_instances.create(
            space_guid=space_guid,
            instance_name=instance_name,
            plan_guid=service_plan_guid,
            accepts_incomplete=True,
        )
        print("Service instance creation in progress for: {}".format(instance_name))
        for i in range(threshold):
            i = i + 1
            service_created = check_service_status(
                client=client, instance_count=i, instance_name=instance_name
            )
            if service_created:
                break
            if i >= 20:
                exception_handler_function(msg=f"Timed out waiting for {instance_name} to reach desired state")
    except Exception as e:
        exception_handler_function(msg=f"Received exception when creating service instance: {instance_name}: {e}")


def check_service_status(
    client,
    instance_count,
    instance_name,
    desired_type="create",
    desired_state="succeeded",
    threshold=20,
):
    for service in client.v2.service_instances:
        if service["entity"]["name"] == instance_name:
            print(
                "Polling to check status of {}, attempt {} of {}".format(
                    instance_name, instance_count, threshold
                )
            )
            if service["entity"]["last_operation"]["type"] == desired_type:
                if service["entity"]["last_operation"]["state"] == desired_state:
                    print(
                        "{} has reached the desired state of {}".format(
                            instance_name, desired_state
                        )
                    )
                    return True
                else:
                    print(
                        "{} is currently in state {}".format(
                            instance_name, service["entity"]["last_operation"]["state"]
                        )
                    )
                    os.system("sleep 60")
                    return False
            else:
                exception_handler_function(msg=f"Excepted last operation to be {desired_type} but got {service['last_operation']['type']}, exiting...")


def service_handler(
    instance_name, organisation, organisation_space, parameters, service_plan
):
    client = cf_client_initialise()
    space_guid = get_space_guid(
        client=client, organisation=organisation, organisation_space=organisation_space
    )
    service_plan_guid = check_service_plan_exists(
        client=client, service_plan=service_plan
    )
    if parameters:
        try:
            service_parameters = json.loads(parameters)
            create_service_with_parameters(
                client=client,
                instance_name=instance_name,
                parameters=service_parameters,
                service_plan_guid=service_plan_guid,
                space_guid=space_guid,
            )
        except json.decoder.JSONDecodeError as e:
            exception_handler_function(msg=f"Could not load service parameters {parameters}: {e}")
    else:
        create_service(
            client=client,
            instance_name=instance_name,
            service_plan_guid=service_plan_guid,
            space_guid=space_guid,
        )
