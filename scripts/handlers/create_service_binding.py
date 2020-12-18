import argparse
import os
import sys

current_dir = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}/../")

from binding import binding_handler


def parse_arguments():
    description = "Arguments for create_service_binding.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-app",
        help="The name of the app to configure binding for",
        dest="app",
        required=True,
    )
    parser.add_argument(
        "-instance-name",
        help="The name of the instance to binding to",
        dest="instance",
        required=True,
    )
    parser.add_argument(
        "-organisation",
        help="The organisation to create resources within",
        dest="organisation",
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
app = args.app
instance = args.instance
organisation = args.organisation
organisation_space = args.space

# Call methods
binding_handler(
    app=app,
    instance=instance,
    organisation=organisation,
    organisation_space=organisation_space,
)
