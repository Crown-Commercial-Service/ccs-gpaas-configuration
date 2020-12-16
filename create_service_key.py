import argparse
import json
from cf_common import get_space_guid, cf_client_initialise


def parse_arguments():
    description = "Arguments for create_service_key.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-organisation",
                        help="The organisation to create resources within",
                        dest="organisation",
                        required=True)
    parser.add_argument("-parameters",
                        help="The paramters to assign to the created service key",
                        dest="parameters",
                        default='{"allow_external_access": true}',
                        required=False)
    parser.add_argument("-service-instance",
                        help="The name of the service instance to use when creating the service key",
                        dest="service_instance",
                        required=True)
    parser.add_argument("-service-key",
                        help="The name of the service key to create",
                        dest="service_key",
                        required=True)
    parser.add_argument("-space",
                        help="The name of the space to create resources for",
                        dest="space",
                        required=True)
    return parser.parse_args()


def check_service_instance_exists(client, service_instance, space_guid):
    service_instance_exists = False
    for service in client.v2.service_instances:
        if service['entity']['space_guid'] == space_guid:
            if service['entity']['name'] == service_instance:
                service_guid = service['metadata']['guid']
                service_instance_exists = True

    if service_instance_exists:
        print(f"Confirmed that service instance for {service_instance} exists")
        return service_guid
    else:
        print(f"Could not find service instance for {service_instance}, exiting...")
        exit(1)


def create_service_key(client, service_guid, service_key_name, parameters):
    try:
        client.v2.service_keys.create(service_instance_guid=service_guid, name=service_key_name, parameters=parameters)
        print(f"Service key {service_key_name} created successfully")
    except Exception as e:
        print(f"Failed to create service key {service_key_name}: {e}")

# Set arguments
args = parse_arguments()
service_instance = args.service_instance
organisation = args.organisation
organisation_space = args.space
parameters = json.loads(args.parameters)
service_key = args.service_key

# Call methods
client = cf_client_initialise()
space_guid = get_space_guid(client=client, organisation=organisation, organisation_space=organisation_space)
service_guid = check_service_instance_exists(client=client, service_instance=service_instance, space_guid=space_guid)
create_service_key(client=client, service_guid=service_guid, service_key_name=service_key, parameters=parameters)
