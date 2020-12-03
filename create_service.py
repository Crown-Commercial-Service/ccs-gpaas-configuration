import argparse
import os
from cf_common import get_space_guid, cf_client_initialise


def parse_arguments():
    description = "Arguments for cf_common.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-instance-name",
                        help="The instance name to give to the service",
                        dest="instance_name",
                        required=True)
    parser.add_argument("-organisation",
                        help="The organisation to create resources within",
                        dest="organisation",
                        required=True)
    parser.add_argument("-service-plan",
                        help="The name of the service plan to create the service for",
                        dest="service_plan",
                        required=True)
    parser.add_argument("-space",
                        help="The name of the space to create resources for",
                        dest="space",
                        required=True)
    return parser.parse_args()


def check_service_plan_exists(client, service_plan):
    service_plan_exists = False
    for plan in client.v2.service_plans:
        if plan['entity']['name'] == service_plan:
            service_plan_exists = True
            service_plan_guid = plan['metadata']['guid']

    if service_plan_exists:
        return service_plan_guid
    else:
        print("Couldnt find service plan")
        exit(1)


def create_first_service(client, instance_name, service_plan_guid, space_guid, threshold=20):
    try:
        client.v2.service_instances.create(space_guid=space_guid, instance_name=instance_name, plan_guid=service_plan_guid, accepts_incomplete=True)
        print("Service instance creation in progress for: {}".format(instance_name))
        for i in range(threshold):
            i = i + 1
            service_created = check_service_status(client=client, instance_count=i, instance_name=instance_name)
            if service_created:
                break
            if i >= 20:
                print("Timed out waiting for {} to reach state".format(instance_name))
                exit(1)
    except Exception as e:
        print("Received exception when creating service instance: {}: {}".format(instance_name, e))


def check_service_status(client, instance_count, instance_name, desired_type='create', desired_state='succeeded', threshold=20):
    for service in client.v2.service_instances:
        if service['entity']['name'] == instance_name:
            print("Polling to check status of {}, attempt {} of {}".format(instance_name, instance_count, threshold))
            if service['entity']['last_operation']['type'] == desired_type:
                if service['entity']['last_operation']['state'] == desired_state:
                    print('{} has reached the desired state of {}'.format(instance_name, desired_state))
                    return True
                else:
                    print('{} is currently in state {}'.format(instance_name, service['entity']['last_operation']['state']))
                    os.system('sleep 60')
                    return False
            else:
                print("Expected last operation to be {} but got {}, exiting...".format(desired_type, service['last_operation']['type']))
                exit(1)


# Set arguments
args = parse_arguments()
instance_name = args.instance_name
organisation = args.organisation
organisation_space = args.space
service_plan = args.service_plan

# Call methods
client = cf_client_initialise()
space_guid = get_space_guid(client=client, organisation=organisation, organisation_space=organisation_space)
service_plan_guid = check_service_plan_exists(client=client, service_plan=service_plan)
create_first_service(client=client, instance_name=instance_name, service_plan_guid=service_plan_guid, space_guid=space_guid)
