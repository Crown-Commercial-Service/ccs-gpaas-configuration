import os
import subprocess
from cf_common import cf_cli_initialise, exception_handler_function
from git import Repo


def clone_github_repository(target_directory, github_repo):
    try:
        Repo.clone_from(github_repo, target_directory)
    except Exception as e:
        exception_handler_function(msg=f"Failed to clone github repo {github_repo}: {e}")


def push_app(
    app_name, home_working_directory, target_directory, manifest_file="manifest.yml"
):
    try:
        os.chdir(target_directory)
        push_app_response = subprocess.call(
            ["cf", "push", app_name, "-f", manifest_file]
        )
        if push_app_response != 0:
            exception_handler_function(
                msg=f"Failed to create domain {app_name}, received return value {push_app_response}"
            )
        print(f"Pushed application: {app_name}")
    except subprocess.CalledProcessError as e:
        exception_handler_function(
            msg=f"Failed to push application {app_name}, received subprocess error: {e}"
        )
        cleanup(
            home_working_directory=home_working_directory,
            target_directory=target_directory,
        )


def cleanup(home_working_directory, target_directory):
    os.chdir(home_working_directory)
    os.system(f"rm -rf {target_directory}")


def app_handler(
    app_name, github_repo, home_working_directory, organisation, organisation_space
):
    target_directory = "{}/{}".format(home_working_directory, app_name)
    client = cf_cli_initialise(organisation=organisation, space=organisation_space)
    clone_github_repository(target_directory=target_directory, github_repo=github_repo)
    push_app(
        app_name=app_name,
        home_working_directory=home_working_directory,
        target_directory=target_directory,
    )
    cleanup(
        home_working_directory=home_working_directory, target_directory=target_directory
    )
