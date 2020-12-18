import argparse
import os
import sys

current_dir = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}/../")

from cf_common import cf_cli_initialise
from domain import create_domain


def parse_arguments():
    description = "Arguments for domain.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-domain-name",
        help="The name of the domain to create",
        dest="domain",
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
domain_name = args.domain
organisation = args.organisation
organisation_space = args.space

# Call methods
cf_cli_initialise(organisation=organisation, space=organisation_space)
create_domain(domain=domain_name, organisation=organisation)
