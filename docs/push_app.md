### Push App
This README outlines the intended behaviour of the [push_app.py](../push_app.py) script, how the script works, required arguments and pre-requisites.

#### Intended Behaviour
The script is intended to allow a user to push an app into their desired organisation and space, using the application's source code and manifest in order
to push the desired configuration.

#### Arguments
- app-name: The name of the app to deploy
- github-repo: The name of the github repository containing your app code & manifest files etc
- organisation: The organisation to create resources within
- space: The name of the space to create resources for

#### How the script works
The script first authenticates against CloudFoundry by calling the *cf_cli_initialise* function from [cf_common.py](../cf_common.py), which will provide access
to the desired organisation and space where you wish to deploy the application to. This function takes the organisation and space arguments, whilst also accessing
the username and password required via environment variables, and authenticates against the default target endpoint.

The script then temporarily clones the application's github repository to it's target directory - this step is required as the cf push needs to occur against the
application's source code. It then uses the cloned repository to run the "cf push" command, using the manifest file as a template (by default, this is set to be mainfest.yml,
but this can be overwritten)

The script then has a final step, which is to perform a cleanup and delete the github repository from the user's home directory, as it is no longer needed at this point.

#### Pre-requisites
- The username and password combination needed to authenticate against CloudFoundry have been exported as environment variables (guser and gpaasword respectively)
- The account you log into has access to push apps to the desired organisation/space
- Python 3.8.3 is installed
- All required pips have been installed (see [requirements.txt](../requirements.txt))
