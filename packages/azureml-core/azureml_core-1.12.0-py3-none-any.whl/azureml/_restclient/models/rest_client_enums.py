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

from enum import Enum


class DataStoreType(Enum):

    azure_blob = "AzureBlob"
    azure_file = "AzureFile"
    gluster_fs = "GlusterFs"
    azure_data_lake = "AzureDataLake"
    azure_my_sql = "AzureMySql"
    azure_sql_database = "AzureSqlDatabase"
    azure_postgre_sql = "AzurePostgreSql"
    dbfs = "DBFS"
    azure_data_lake_gen2 = "AzureDataLakeGen2"


class AzureStorageCredentialTypes(Enum):

    none = "None"
    sas = "Sas"
    account_key = "AccountKey"
    client_credentials = "ClientCredentials"


class SqlCredentialTypes(Enum):

    sql_authentication = "SqlAuthentication"
    service_principal = "ServicePrincipal"
    none = "None"


class OrderString(Enum):

    created_at_desc = "CreatedAtDesc"
    created_at_asc = "CreatedAtAsc"
    updated_at_desc = "UpdatedAtDesc"
    updated_at_asc = "UpdatedAtAsc"


class AsyncOperationState(Enum):

    not_started = "NotStarted"
    running = "Running"
    cancelled = "Cancelled"
    succeeded = "Succeeded"
    failed = "Failed"
    timed_out = "TimedOut"


class WebServiceState(Enum):

    transitioning = "Transitioning"
    healthy = "Healthy"
    unhealthy = "Unhealthy"
    failed = "Failed"
    unschedulable = "Unschedulable"


class DeploymentType(Enum):

    grpc_realtime_endpoint = "GRPCRealtimeEndpoint"
    http_realtime_endpoint = "HttpRealtimeEndpoint"
    batch = "Batch"


class DeployedApiFlavor(Enum):

    azure_ml_app = "AzureMlApp"
    functions_app = "FunctionsApp"


class ArchitectureType(Enum):

    amd64 = "Amd64"
    arm32v7 = "Arm32v7"


class OSType(Enum):

    linux = "Linux"
    windows = "Windows"


class RuntimeType(Enum):

    spark_python = "SparkPython"
    python = "Python"
    python_slim = "PythonSlim"
    python_custom = "PythonCustom"


class ImageType(Enum):

    docker = "Docker"


class VariantType(Enum):

    control = "Control"
    treatment = "Treatment"


class DatasetConsumptionType(Enum):

    run_input = "RunInput"
    reference = "Reference"


class DatasetDeliveryMechanism(Enum):

    direct = "Direct"
    mount = "Mount"
    download = "Download"


class DatasetOutputType(Enum):

    run_output = "RunOutput"
    reference = "Reference"


class DatasetOutputMechanism(Enum):

    upload = "Upload"
    mount = "Mount"


class ProvisioningState(Enum):

    unknown = "Unknown"
    updating = "Updating"
    creating = "Creating"
    deleting = "Deleting"
    succeeded = "Succeeded"
    failed = "Failed"
    canceled = "Canceled"


class EncryptionStatus(Enum):

    enabled = "Enabled"
    disabled = "Disabled"


class PrivateEndpointServiceConnectionStatus(Enum):

    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
    disconnected = "Disconnected"
    timeout = "Timeout"


class PrivateEndpointConnectionProvisioningState(Enum):

    succeeded = "Succeeded"
    creating = "Creating"
    deleting = "Deleting"
    failed = "Failed"


class UsageUnit(Enum):

    count = "Count"


class QuotaUnit(Enum):

    count = "Count"


class Status(Enum):

    undefined = "Undefined"
    success = "Success"
    failure = "Failure"
    invalid_quota_below_cluster_minimum = "InvalidQuotaBelowClusterMinimum"
    invalid_quota_exceeds_subscription_limit = "InvalidQuotaExceedsSubscriptionLimit"
    invalid_vm_family_name = "InvalidVMFamilyName"
    operation_not_supported_for_sku = "OperationNotSupportedForSku"
    operation_not_enabled_for_region = "OperationNotEnabledForRegion"


class ResourceIdentityType(Enum):

    system_assigned = "SystemAssigned"
    user_assigned = "UserAssigned"
    system_assigned_user_assigned = "SystemAssigned, UserAssigned"
    none = "None"


class VmPriority(Enum):

    dedicated = "Dedicated"
    low_priority = "LowPriority"


class RemoteLoginPortPublicAccess(Enum):

    enabled = "Enabled"
    disabled = "Disabled"
    not_specified = "NotSpecified"


class AllocationState(Enum):

    steady = "Steady"
    resizing = "Resizing"


class NodeState(Enum):

    idle = "idle"
    running = "running"
    preparing = "preparing"
    unusable = "unusable"
    leaving = "leaving"
    preempted = "preempted"


class ComputeType(Enum):

    aks = "AKS"
    aml_compute = "AmlCompute"
    data_factory = "DataFactory"
    virtual_machine = "VirtualMachine"
    hd_insight = "HDInsight"
    databricks = "Databricks"
    data_lake_analytics = "DataLakeAnalytics"


class ReasonCode(Enum):

    not_specified = "NotSpecified"
    not_available_for_region = "NotAvailableForRegion"
    not_available_for_subscription = "NotAvailableForSubscription"


class UnderlyingResourceAction(Enum):

    delete = "Delete"
    detach = "Detach"
