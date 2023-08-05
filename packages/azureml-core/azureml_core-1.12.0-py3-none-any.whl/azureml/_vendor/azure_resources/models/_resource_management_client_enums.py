# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from enum import Enum


class DeploymentMode(str, Enum):

    incremental = "Incremental"
    complete = "Complete"


class OnErrorDeploymentType(str, Enum):

    last_successful = "LastSuccessful"
    specific_deployment = "SpecificDeployment"


class WhatIfResultFormat(str, Enum):

    resource_id_only = "ResourceIdOnly"
    full_resource_payloads = "FullResourcePayloads"


class ResourceIdentityType(str, Enum):

    system_assigned = "SystemAssigned"
    user_assigned = "UserAssigned"
    system_assigned_user_assigned = "SystemAssigned, UserAssigned"
    none = "None"


class PropertyChangeType(str, Enum):

    create = "Create"  #: The property does not exist in the current state but is present in the desired state. The property will be created when the deployment is executed.
    delete = "Delete"  #: The property exists in the current state and is missing from the desired state. It will be deleted when the deployment is executed.
    modify = "Modify"  #: The property exists in both current and desired state and is different. The value of the property will change when the deployment is executed.
    array = "Array"  #: The property is an array and contains nested changes.


class ChangeType(str, Enum):

    create = "Create"  #: The resource does not exist in the current state but is present in the desired state. The resource will be created when the deployment is executed.
    delete = "Delete"  #: The resource exists in the current state and is missing from the desired state. The resource will be deleted when the deployment is executed.
    ignore = "Ignore"  #: The resource exists in the current state and is missing from the desired state. The resource will not be deployed or modified when the deployment is executed.
    deploy = "Deploy"  #: The resource exists in the current state and the desired state and will be redeployed when the deployment is executed. The properties of the resource may or may not change.
    no_change = "NoChange"  #: The resource exists in the current state and the desired state and will be redeployed when the deployment is executed. The properties of the resource will not change.
    modify = "Modify"  #: The resource exists in the current state and the desired state and will be redeployed when the deployment is executed. The properties of the resource will change.
