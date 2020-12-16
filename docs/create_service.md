### Create Service
This README outlines the intended behaviour of the [create_service.py](../scripts/create_service.py) script, how the script works, required arguments and pre-requisites.

#### Intended Behaviour
The script is intended to allow a user to provision a backing service within a given GPaaS Organisation/Space

#### Arguments
- instance-name: The instance name to give to the service
- organisation: The organisation to create resources within
- service-plan: The name of the service plan to create the service for
- space: The name of the space to create resources for

#### How the script works
The script first authenticates against CloudFoundry by calling the *cf_client_initialise* function from [cf_common.py](../scripts/cf_common.py), which will authenticate against
the cloudfoundry-client, using the provided username/password combination (these are passed in as environment variables, guser and gpaasword respectively) - the cloudfoundry-client
will then be used within the script in order to create the backing service.

The script then retrieves the "space-guid" - this is the ID of the space, which is needed by the cloudfoundry-client in order to be able to create the service in the desired
space. The value returned is the guid of the space you provide via the relevant argument. Additionally, the script needs to retrieve the service plan's guid.

The script will then create the backing service using the cloudfoundry-client, creating the desired service in the appropriate space with the appropriate plan. The script will then
continue to poll the status of the backing service to ensure that it finishes provisioning successfully.

#### Pre-requisites
- The username and password combination needed to authenticate against CloudFoundry have been exported as environment variables (guser and gpaasword respectively)
- The account you log into has access to push apps to the desired organisation/space
- Python 3.8.3 is installed
- All required pips have been installed (see [requirements.txt](../requirements.txt))
