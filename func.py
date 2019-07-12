import logging
import sys
import oci.auth
import oci.functions

from oci import identity
from oci import pagination




def get_compartment(signer, tenancy, compartment_name):
    """
    Identifies compartment ID by its name within the particular tenancy
    :param oci_cfg: OCI auth config
    :param compartment_name: OCI tenancy compartment name
    :return: OCI tenancy compartment
    """
    identity_client = identity.IdentityClient(config={}, signer=signer)
    result = pagination.list_call_get_all_results(
        identity_client.list_compartments,
        tenancy,
        compartment_id_in_subtree=True,
        access_level="ACCESSIBLE",
    )
    for c in result.data:
        if compartment_name == c.name:
            print(type(c))
            return c

    raise Exception("compartment not found")

def get_app(functions_client, app_name, compartment):
    """
    Identifies app object by its name
    :param functions_client: OCI Functions client
    :type functions_client: oci.functions.FunctionsManagementClient
    :param app_name: OCI Functions app name
    :type app_name: str
    :param compartment: OCI tenancy compartment
    :type compartment: oci.identity.models.Compartment
    :return: OCI Functions app
    :rtype: oci.functions.models.Application
    """
    result = pagination.list_call_get_all_results(
        functions_client.list_applications,
        compartment.id
    )
    for app in result.data:
        if app_name == app.display_name:
            print(type(app))
            print(app.display_name)
            return app

    raise Exception("app not found")

def get_function(functions_client, app, function_name):
    """
    Identifies function object by its name
    :param functions_client: OCI Functions client
    :type functions_client: oci.functions.FunctionsManagementClient
    :param app: OCI Functions app
    :type app: oci.functions.models.Application
    :param function_name: OCI Functions function name
    :type function_name: str
    :return: OCI Functions function
    :rtype: oci.functions.models.Function
    """
    result = pagination.list_call_get_all_results(
        functions_client.list_functions,
        app.id
    )
    for fn in result.data:
        if function_name == fn.display_name:
            print(type(fn))
            print(fn.display_name)
            return fn

    raise Exception("function not found")


def main():
    if (len(sys.argv) != 4) & (len(sys.argv) != 5):
        raise Exception("usage: python invoke_function.py"
                        " <compartment-name> <app-name> "
                        "<function-name> <request payload>")

    compartment_name = sys.argv[1]
    app_name = sys.argv[2]
    fn_name = sys.argv[3]
    fn_body = None
    if (len(sys.argv) == 5):
        fn_body = sys.argv[4]

    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    signer.refresh_security_token()

    tenancy = signer.tenancy_id

    functions_client = oci.functions.FunctionsManagementClient(config={}, signer=signer)

    compartment = get_compartment(signer=signer, tenancy=tenancy, compartment_name=compartment_name )

    app = get_app(functions_client, app_name, compartment)

    fn = get_function(functions_client, app, fn_name)

    invoke_client = oci.functions.FunctionsInvokeClient(config={}, signer=signer, service_endpoint=fn.invoke_endpoint)
    if fn_body != None:
        resp = invoke_client.invoke_function(fn.id, invoke_function_body=sys.argv[4])
    else:
        resp = invoke_client.invoke_function(fn.id)

    print(resp.data.text)

if __name__ == '__main__':
    main()
