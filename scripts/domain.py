import subprocess
from cf_common import exception_handler_function


def create_domain(domain, organisation):
    try:
        print(f"Creating domain {domain} for {organisation}")
        create_domain_response = subprocess.call(
            ["cf", "create-domain", organisation, domain]
        )
        if create_domain_response != 0:
            exception_handler_function(
                msg=f"Failed to create domain {domain}, received return value {create_domain_response}"
            )
        print(f"Created domain: {domain}")
    except subprocess.CalledProcessError as e:
        exception_handler_function(
            msg=f"Failed to create domain {domain}, received subprocess error: {e}"
        )
