# Using Instance Principals to Invoke an Oracle Function from an OCI Compute Instance Virtual Machine

  This function uses Instance Principals to authenticate a call to OCI Services to invoke an Oracle Function call.

  Uses the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html) to create a client that gets access to OCI Object Storage.

  In this example we'll show how you can invoke an Oracle Function from a VM with only the desired compartment name, application name, the function name, and a request payload by using an Instance Principal Security Signer to get authentication from your Compute Instance. We will use three API Clients exposed by the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html).


  1. [IdentityClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/identity/client/oci.identity.IdentityClient.html) is an API for managing users, groups, compartments, and policies, we will use it to find the compartment's OCID from its name.

  2. [FunctionsManagementClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/functions/client/oci.functions.FunctionsManagementClient.html) - is used for functions lifecycle management operations including creating, updating, and querying applications and functions


  3. [FunctionsInvokeClient](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/functions/client/oci.functions.FunctionsInvokeClient.html#oci.functions.FunctionsInvokeClient) - is used specifically for invoking functions

  As you make your way through this tutorial, look out for this icon. ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE) Whenever you see it, it's time for you to perform an action.

  For more information on code structure and API along with the data types please read code doc strings available for each method:

  * [`get_compartment`](https://github.com/arodri202/oci-python-invoke-function-ip/blob/master/func.py#L12) method
  * [`get_app`](https://github.com/arodri202/oci-python-invoke-function-ip/blob/master/func.py#L33) method
  * [`get_function`](https://github.com/arodri202/oci-python-invoke-function-ip/blob/master/func.py#L57) method


Pre-requisites:
---------------
  1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

  2. Make sure you have a function to invoke, if not follow [this guide](https://github.com/fnproject/fn/blob/master/README.md#your-first-function) to create one.

  3. Have an instance ready with pip, python, and git. If you do not have an instance ready, follow [this guide](https://docs.cloud.oracle.com/iaas/Content/Compute/Concepts/computeoverview.htm) to create one.

  4. Have a dynamic group and corresponding policies, if you do not have them, follow [this guide](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/callingservicesfrominstances.htm)

  5. Install OCI Python SDK in a VirutalEnv in your instance

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)

  python3
  ```
  pip3 install virutalenv
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install oci
  ```

  python2
  ```
  pip install virutalenv
  python -m virtualenv .venv
  source .venv/bin/activate
  pip install oci
  ```

  6. Clone this repository in a directory in your instance

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  git clone https://github.com/arodri202/oci-python-invoke-function-ip.git
  ```

  7. Change to the correct directory where you cloned the example:

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  cd oci-python-invoke-function-ip
  ```

Invoke the Function!
--------------------

  ![user input icon](https://raw.githubusercontent.com/arodri202/oci-python-object-storage/master/images/userinput.png?token=AK4AYAVV2EYKYR4LI72BV6S5CUJZE)
  ```
  python invoke_function.py <compartment-name> <app-name> <function-name> <request payload>
  ```
  e.g.
  ```
  python invoke_function.py workshop helloworld-app helloworld-func-go '{"name":"foobar"}'
  ```
  Upon success, you should see the expected output of your function.
