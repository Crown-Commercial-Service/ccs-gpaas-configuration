import argparse
import os
import subprocess
from cf_common import cf_cli_initialise, run
from git import Repo


def parse_arguments():
    description = "Arguments for cf_common.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-app-name",
                        help="The name of the app to deploy",
                        dest="app_name",
                        required=True)
    parser.add_argument("-github-repo",
                        help="The name of the github repository containing your app code & manifest files etc",
                        dest="github_repo",
                        required=True)
    parser.add_argument("-organisation",
                        help="The organisation to create resources within",
                        dest="organisation",
                        required=True)
    parser.add_argument("-space",
                        help="The name of the space to create resources for",
                        dest="space",
                        required=True)
    parser.add_argument("-subdomain",
                        help="The subdomain for the application (optional)",
                        dest="subdomain",
                        required=False)
    return parser.parse_args()


def clone_github_repository(target_directory, github_repo):
    try:
        Repo.clone_from(github_repo, target_directory)
    except Exception as e:
        print("Failed to clone github repo {}: {}".format(github_repo, e))


def push_app(app_name, home_working_directory, target_directory, manifest_file='manifest.yml'):
    try:
        os.chdir(target_directory)
        run(['cf', 'push', app_name, '-f', manifest_file])
        print(f'Pushed application: {app_name}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to push application {app_name}: {e}')
        cleanup(home_working_directory=home_working_directory, target_directory=target_directory)


def cleanup(home_working_directory, target_directory):
    os.chdir(home_working_directory)
    os.system(f'rm -rf {target_directory}')


# Set arguments
args = parse_arguments()
app_name = args.app_name
github_repo = args.github_repo
organisation = args.organisation
organisation_space = args.space
subdomain = args.subdomain

home_working_directory = os.getcwd()
target_directory = '{}/{}'.format(home_working_directory, app_name)
client = cf_cli_initialise(organisation=organisation, space=organisation_space)
clone_github_repository(target_directory=target_directory, github_repo=github_repo)
push_app(app_name=app_name, home_working_directory=home_working_directory, target_directory=target_directory)
cleanup(home_working_directory=home_working_directory, target_directory=target_directory)
