import argparse
import json
import os
import sys

current_dir = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}/../")

from service_key import service_key_handler


def parse_arguments():
    description = "Arguments for service_key.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-organisation",
        help="The organisation to create resources within",
        dest="organisation",
        required=True,
    )
    parser.add_argument(
        "-parameters",
        help="The paramters to assign to the created service key",
        dest="parameters",
        default='{"allow_external_access": true}',
        required=False,
    )
    parser.add_argument(
        "-service-instance",
        help="The name of the service instance to use when creating the service key",
        dest="service_instance",
        required=True,
    )
    parser.add_argument(
        "-service-key",
        help="The name of the service key to create",
        dest="service_key",
        required=True,
    )
    parser.add_argument(
        "-space",
        help="The name of the space to create resources for",
        dest="space",
        required=True,
    )
    return parser.parse_args()


# Set arguments
args = parse_arguments()
service_instance = args.service_instance
organisation = args.organisation
organisation_space = args.space
parameters = json.loads(args.parameters)
service_key = args.service_key

service_key_handler(
    organisation=organisation,
    organisation_space=organisation_space,
    parameters=parameters,
    service_instance=service_instance,
    service_key=service_key,
)
