import argparse
import subprocess
from scripts.cf_common import run, cf_cli_initialise


def parse_arguments():
    description = "Arguments for create_domain.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-domain-name",
                        help="The name of the domain to create",
                        dest="domain",
                        required=True)
    parser.add_argument("-organisation",
                        help="The organisation to create resources within",
                        dest="organisation",
                        required=True)
    parser.add_argument("-space",
                        help="The name of the space to create resources for",
                        dest="space",
                        required=True)
    return parser.parse_args()


def create_domain(domain, organisation):
    try:
        print(f'Creating domain {domain} for {organisation}')
        run(['cf', 'create-domain', organisation, domain])
        print(f'Created domain: {domain}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to create domain {domain}: {e}')


# Set arguments
args = parse_arguments()
domain_name = args.domain
organisation = args.organisation
organisation_space = args.space

# Call methods
client = cf_cli_initialise(organisation=organisation, space=organisation_space)
create_domain(domain=domain_name, organisation=organisation)
