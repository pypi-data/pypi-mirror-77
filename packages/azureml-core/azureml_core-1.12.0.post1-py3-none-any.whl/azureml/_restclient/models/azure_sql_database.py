# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AzureSqlDatabase(Model):
    """AzureSqlDatabase.

    :param server_name: The Azure SQL server name
    :type server_name: str
    :param database_name: The Azure SQL database name
    :type database_name: str
    :param endpoint: The server host endpoint
    :type endpoint: str
    :param user_id: The Azure SQL user id
    :type user_id: str
    :param user_password: The Azure SQL user password
    :type user_password: str
    :param port_number: The Azure SQL port number
    :type port_number: str
    :param credential_type: Sql Authentication type. Possible values include:
     'SqlAuthentication', 'ServicePrincipal', 'None'
    :type credential_type: str or ~_restclient.models.SqlCredentialTypes
    :param client_id: The Client ID/Application ID
    :type client_id: str
    :param tenant_id: The ID of the tenant the service principal/app belongs
     to
    :type tenant_id: str
    :param is_cert_auth: Is it using certificate to authenticate. If false
     then use client secret
    :type is_cert_auth: bool
    :param certificate: The content of the certificate used for authentication
    :type certificate: str
    :param thumbprint: The thumbprint of the certificate above
    :type thumbprint: str
    :param client_secret: The client secret
    :type client_secret: str
    :param authority_url: The authority URL used for authentication
    :type authority_url: str
    :param resource_uri: The resource the service principal/app has access to
    :type resource_uri: str
    :param subscription_id: Subscription Id
    :type subscription_id: str
    :param resource_group: Resource Group Name
    :type resource_group: str
    """

    _attribute_map = {
        'server_name': {'key': 'serverName', 'type': 'str'},
        'database_name': {'key': 'databaseName', 'type': 'str'},
        'endpoint': {'key': 'endpoint', 'type': 'str'},
        'user_id': {'key': 'userId', 'type': 'str'},
        'user_password': {'key': 'userPassword', 'type': 'str'},
        'port_number': {'key': 'portNumber', 'type': 'str'},
        'credential_type': {'key': 'credentialType', 'type': 'SqlCredentialTypes'},
        'client_id': {'key': 'clientId', 'type': 'str'},
        'tenant_id': {'key': 'tenantId', 'type': 'str'},
        'is_cert_auth': {'key': 'isCertAuth', 'type': 'bool'},
        'certificate': {'key': 'certificate', 'type': 'str'},
        'thumbprint': {'key': 'thumbprint', 'type': 'str'},
        'client_secret': {'key': 'clientSecret', 'type': 'str'},
        'authority_url': {'key': 'authorityUrl', 'type': 'str'},
        'resource_uri': {'key': 'resourceUri', 'type': 'str'},
        'subscription_id': {'key': 'subscriptionId', 'type': 'str'},
        'resource_group': {'key': 'resourceGroup', 'type': 'str'},
    }

    def __init__(self, server_name=None, database_name=None, endpoint=None, user_id=None, user_password=None, port_number=None, credential_type=None, client_id=None, tenant_id=None, is_cert_auth=None, certificate=None, thumbprint=None, client_secret=None, authority_url=None, resource_uri=None, subscription_id=None, resource_group=None):
        super(AzureSqlDatabase, self).__init__()
        self.server_name = server_name
        self.database_name = database_name
        self.endpoint = endpoint
        self.user_id = user_id
        self.user_password = user_password
        self.port_number = port_number
        self.credential_type = credential_type
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.is_cert_auth = is_cert_auth
        self.certificate = certificate
        self.thumbprint = thumbprint
        self.client_secret = client_secret
        self.authority_url = authority_url
        self.resource_uri = resource_uri
        self.subscription_id = subscription_id
        self.resource_group = resource_group
