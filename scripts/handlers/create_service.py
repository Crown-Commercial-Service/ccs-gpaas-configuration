import argparse
import os
import sys

current_dir = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}/../")

from service import service_handler


def parse_arguments():
    description = "Arguments for create_service.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-instance-name",
        help="The instance name to give to the service",
        dest="instance_name",
        required=True,
    )
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
        required=False,
    )
    parser.add_argument(
        "-service-plan",
        help="The name of the service plan to create the service for",
        dest="service_plan",
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
instance_name = args.instance_name
organisation = args.organisation
organisation_space = args.space
parameters = args.parameters
service_plan = args.service_plan

# Call methods
service_handler(
    instance_name=instance_name,
    organisation=organisation,
    organisation_space=organisation_space,
    parameters=parameters,
    service_plan=service_plan,
)
