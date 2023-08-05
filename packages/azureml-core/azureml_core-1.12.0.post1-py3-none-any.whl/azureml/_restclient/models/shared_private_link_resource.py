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


class SharedPrivateLinkResource(Model):
    """SharedPrivateLinkResource.

    :param name: Unique name of the private link.
    :type name: str
    :param private_link_resource_id: The resource id that private link links
     to.
    :type private_link_resource_id: str
    :param group_id: The private link resource group id.
    :type group_id: str
    :param request_message: Request message.
    :type request_message: str
    :param status: Indicates whether the connection has been
     Approved/Rejected/Removed by the owner of the service. Possible values
     include: 'Pending', 'Approved', 'Rejected', 'Disconnected', 'Timeout'
    :type status: str or
     ~_restclient.models.PrivateEndpointServiceConnectionStatus
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'private_link_resource_id': {'key': 'properties.privateLinkResourceId', 'type': 'str'},
        'group_id': {'key': 'properties.groupId', 'type': 'str'},
        'request_message': {'key': 'properties.requestMessage', 'type': 'str'},
        'status': {'key': 'properties.status', 'type': 'str'},
    }

    def __init__(self, name=None, private_link_resource_id=None, group_id=None, request_message=None, status=None):
        super(SharedPrivateLinkResource, self).__init__()
        self.name = name
        self.private_link_resource_id = private_link_resource_id
        self.group_id = group_id
        self.request_message = request_message
        self.status = status
