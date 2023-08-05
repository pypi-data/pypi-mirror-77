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

from .vnet_configuration import VnetConfiguration


class ACIServiceCreateRequestVnetConfiguration(VnetConfiguration):
    """VnetConfiguration.

    :param vnet_name: vnetName
    :type vnet_name: str
    :param subnet_name: subnetName
    :type subnet_name: str
    """

    def __init__(self, vnet_name=None, subnet_name=None):
        super(ACIServiceCreateRequestVnetConfiguration, self).__init__(vnet_name=vnet_name, subnet_name=subnet_name)
