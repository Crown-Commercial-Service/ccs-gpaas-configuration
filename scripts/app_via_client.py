import os
from cf_common import (
    cf_cli_initialise,
    exception_handler_function,
    cf_client_initialise,
    get_space_guid,
)
from cloudfoundry_client.operations.push.push import PushOperation
from git import Repo


def clone_github_repository(target_directory, github_repo):
    try:
        Repo.clone_from(github_repo, target_directory)
    except Exception as e:
        print("Failed to clone github repo {}: {}".format(github_repo, e))


def push_application(
    app, client, home_working_directory, manifest_path, space_guid, target_directory
):
    try:
        os.chdir(target_directory)
        print("Attempting to push application...")
        PushOperation(client=client).push(
            space_id=space_guid, manifest_path=manifest_path
        )
        print(f"Successfully pushed application: {app}")
        cleanup(
            home_working_directory=home_working_directory,
            target_directory=target_directory,
        )
    except Exception as e:
        cleanup(
            home_working_directory=home_working_directory,
            target_directory=target_directory,
        )
        exception_handler_function(
            msg=f"Failed to push application {app}, received subprocess error: {e}"
        )


def cleanup(home_working_directory, target_directory):
    os.chdir(home_working_directory)
    os.system(f"rm -rf {target_directory}")


def app_handler(app, github_repo, home_working_directory, organisation, organisation_space, manifest_path="manifest.yml"):
    client = cf_client_initialise()
    target_directory = "{}/{}".format(home_working_directory, app)

    space_guid = get_space_guid(
        client=client,
        organisation=organisation,
        organisation_space=organisation_space,
    )
    clone_github_repository(github_repo=github_repo, target_directory=target_directory)
    push_application(
        app=app,
        client=client,
        home_working_directory=home_working_directory,
        manifest_path=manifest_path,
        space_guid=space_guid,
        target_directory=target_directory,
    )
