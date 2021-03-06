import os
import subprocess
import urllib3
from cloudfoundry_client.client import CloudFoundryClient

urllib3.disable_warnings()


# Backport for subprocess.run
def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if "stdin" in kwargs:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr
        )
    return retcode, stdout, stderr


def cf_cli_initialise(
    organisation, space, target_endpoint="api.london.cloud.service.gov.uk"
):
    try:
        run(
            [
                "cf",
                "login",
                "-a",
                target_endpoint,
                "-u",
                os.environ["guser"],
                "-p",
                os.environ["gpaasword"],
                "-o",
                organisation,
                "-s",
                space,
            ]
        )
    except subprocess.CalledProcessError as e:
        exception_handler_function(
            msg=f"Failed to login to {organisation} {space}: {e}"
        )


def cf_client_initialise():
    target_endpoint = "https://api.london.cloud.service.gov.uk/"
    proxy = dict(
        http=os.environ.get("HTTP_PROXY", ""), https=os.environ.get("HTTPS_PROXY", "")
    )
    client = CloudFoundryClient(target_endpoint, proxy=proxy, verify=False)
    client.init_with_user_credentials(os.environ["guser"], os.environ["gpaasword"])
    return client


def get_space_guid(client, organisation, organisation_space):
    for org in client.v2.organizations:
        if organisation == org["entity"]["name"]:
            for space in org.spaces():
                if organisation_space == space["entity"]["name"]:
                    space_guid = space["metadata"]["guid"]
                    return space_guid


def get_guid_within_space(client_search, identifier, space_guid):
    identifier_exists = False
    for config in client_search:
        if config["entity"]["space_guid"] == space_guid:
            if config["entity"]["name"] == identifier:
                identifier_exists = True
                identifier_guid = config["metadata"]["guid"]

    if identifier_exists:
        return identifier_guid
    else:
        exception_handler_function(msg=f"Failed to find the guid for {identifier}")


def exception_handler_function(msg):
    print(f"Encountered exception: {msg}")
    exit(1)
