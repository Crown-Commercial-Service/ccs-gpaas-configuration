import argparse
import os
import sys

current_dir = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}/../")
from app import app_handler


def parse_arguments():
    description = "Arguments for cf_common.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-app-name",
        help="The name of the app to deploy",
        dest="app_name",
        required=True,
    )
    parser.add_argument(
        "-github-repo",
        help="The name of the github repository containing your app code & manifest files etc",
        dest="github_repo",
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
    parser.add_argument(
        "-subdomain",
        help="The subdomain for the application (optional)",
        dest="subdomain",
        required=False,
    )
    return parser.parse_args()


# Set arguments
args = parse_arguments()
app_name = args.app_name
github_repo = args.github_repo
organisation = args.organisation
organisation_space = args.space
subdomain = args.subdomain

app_handler(
    app_name=app_name,
    github_repo=github_repo,
    organisation=organisation,
    organisation_space=organisation_space,
    home_working_directory=os.getcwd(),
)
