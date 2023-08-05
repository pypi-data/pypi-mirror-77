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

from .aks_variant_response import AKSVariantResponse


class AKSServiceResponse(AKSVariantResponse):
    """The response for an AKS service.

    :param id: The service Id.
    :type id: str
    :param name: The service name.
    :type name: str
    :param description: The service description.
    :type description: str
    :param kv_tags: The service tag dictionary. Tags are mutable.
    :type kv_tags: dict[str, str]
    :param properties: The service property dictionary. Properties are
     immutable.
    :type properties: dict[str, str]
    :param operation_id: The ID of the latest asynchronous operation for this
     service.
    :type operation_id: str
    :param state: The current state of the service. Possible values include:
     'Transitioning', 'Healthy', 'Unhealthy', 'Failed', 'Unschedulable'
    :type state: str or ~_restclient.models.WebServiceState
    :param created_time: The time the service was created.
    :type created_time: datetime
    :param updated_time: The time the service was updated.
    :type updated_time: datetime
    :param error: The error details.
    :type error: ~_restclient.models.ServiceResponseBaseError
    :param deployment_type: The deployment type for the service. Possible
     values include: 'GRPCRealtimeEndpoint', 'HttpRealtimeEndpoint', 'Batch'
    :type deployment_type: str or ~_restclient.models.DeploymentType
    :param created_by: The individual last responsible for creating or
     updating the service.
    :type created_by: ~_restclient.models.ServiceResponseBaseCreatedBy
    :param compute_type: Constant filled by server.
    :type compute_type: str
    :param is_default: Is this the default variant.
    :type is_default: bool
    :param traffic_percentile: The amount of traffic variant receives.
    :type traffic_percentile: float
    :param type: The type of the variant. Possible values include: 'Control',
     'Treatment'
    :type type: str or ~_restclient.models.VariantType
    :param image_details: The Docker Image details.
    :type image_details: ~_restclient.models.AKSServiceResponseImageDetails
    :param image_id: The Id of the Image.
    :type image_id: str
    :param image_digest: The Digest of the Image.
    :type image_digest: str
    :param models_property: The list of models.
    :type models_property: list[~_restclient.models.Model]
    :param container_resource_requirements: The container resource
     requirements.
    :type container_resource_requirements:
     ~_restclient.models.AKSServiceResponseContainerResourceRequirements
    :param max_concurrent_requests_per_container: The maximum number of
     concurrent requests per container.
    :type max_concurrent_requests_per_container: int
    :param max_queue_wait_ms: Maximum time a request will wait in the queue
     (in milliseconds). After this time, the service will return 503 (Service
     Unavailable)
    :type max_queue_wait_ms: int
    :param compute_name: The name of the compute resource.
    :type compute_name: str
    :param namespace: The Kubernetes namespace of the deployment.
    :type namespace: str
    :param num_replicas: The number of replicas on the cluster.
    :type num_replicas: int
    :param data_collection: Details of the data collection options specified.
    :type data_collection:
     ~_restclient.models.AKSServiceResponseDataCollection
    :param app_insights_enabled: Whether or not Application Insights is
     enabled.
    :type app_insights_enabled: bool
    :param auto_scaler: The auto scaler properties.
    :type auto_scaler: ~_restclient.models.AKSServiceResponseAutoScaler
    :param scoring_uri: The Uri for sending scoring requests.
    :type scoring_uri: str
    :param deployment_status: The deployment status.
    :type deployment_status:
     ~_restclient.models.AKSServiceResponseDeploymentStatus
    :param scoring_timeout_ms: The scoring timeout in milliseconds.
    :type scoring_timeout_ms: int
    :param liveness_probe_requirements: The liveness probe requirements.
    :type liveness_probe_requirements:
     ~_restclient.models.AKSServiceResponseLivenessProbeRequirements
    :param auth_enabled: Whether or not authentication is enabled.
    :type auth_enabled: bool
    :param aad_auth_enabled: Whether or not AAD authentication is enabled.
    :type aad_auth_enabled: bool
    :param swagger_uri: The Uri for sending swagger requests.
    :type swagger_uri: str
    :param model_config_map: Details on the models and configurations.
    :type model_config_map: dict[str, object]
    :param environment_image_request: The Environment, models and assets used
     for inferencing.
    :type environment_image_request:
     ~_restclient.models.AKSServiceResponseEnvironmentImageRequest
    """

    _validation = {
        'compute_type': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'kv_tags': {'key': 'kvTags', 'type': '{str}'},
        'properties': {'key': 'properties', 'type': '{str}'},
        'operation_id': {'key': 'operationId', 'type': 'str'},
        'state': {'key': 'state', 'type': 'WebServiceState'},
        'created_time': {'key': 'createdTime', 'type': 'iso-8601'},
        'updated_time': {'key': 'updatedTime', 'type': 'iso-8601'},
        'error': {'key': 'error', 'type': 'ServiceResponseBaseError'},
        'deployment_type': {'key': 'deploymentType', 'type': 'DeploymentType'},
        'created_by': {'key': 'createdBy', 'type': 'ServiceResponseBaseCreatedBy'},
        'compute_type': {'key': 'computeType', 'type': 'str'},
        'is_default': {'key': 'isDefault', 'type': 'bool'},
        'traffic_percentile': {'key': 'trafficPercentile', 'type': 'float'},
        'type': {'key': 'type', 'type': 'VariantType'},
        'image_details': {'key': 'imageDetails', 'type': 'AKSServiceResponseImageDetails'},
        'image_id': {'key': 'imageId', 'type': 'str'},
        'image_digest': {'key': 'imageDigest', 'type': 'str'},
        'models_property': {'key': 'models', 'type': '[Model]'},
        'container_resource_requirements': {'key': 'containerResourceRequirements', 'type': 'AKSServiceResponseContainerResourceRequirements'},
        'max_concurrent_requests_per_container': {'key': 'maxConcurrentRequestsPerContainer', 'type': 'int'},
        'max_queue_wait_ms': {'key': 'maxQueueWaitMs', 'type': 'int'},
        'compute_name': {'key': 'computeName', 'type': 'str'},
        'namespace': {'key': 'namespace', 'type': 'str'},
        'num_replicas': {'key': 'numReplicas', 'type': 'int'},
        'data_collection': {'key': 'dataCollection', 'type': 'AKSServiceResponseDataCollection'},
        'app_insights_enabled': {'key': 'appInsightsEnabled', 'type': 'bool'},
        'auto_scaler': {'key': 'autoScaler', 'type': 'AKSServiceResponseAutoScaler'},
        'scoring_uri': {'key': 'scoringUri', 'type': 'str'},
        'deployment_status': {'key': 'deploymentStatus', 'type': 'AKSServiceResponseDeploymentStatus'},
        'scoring_timeout_ms': {'key': 'scoringTimeoutMs', 'type': 'int'},
        'liveness_probe_requirements': {'key': 'livenessProbeRequirements', 'type': 'AKSServiceResponseLivenessProbeRequirements'},
        'auth_enabled': {'key': 'authEnabled', 'type': 'bool'},
        'aad_auth_enabled': {'key': 'aadAuthEnabled', 'type': 'bool'},
        'swagger_uri': {'key': 'swaggerUri', 'type': 'str'},
        'model_config_map': {'key': 'modelConfigMap', 'type': '{object}'},
        'environment_image_request': {'key': 'environmentImageRequest', 'type': 'AKSServiceResponseEnvironmentImageRequest'},
    }

    def __init__(self, id=None, name=None, description=None, kv_tags=None, properties=None, operation_id=None, state=None, created_time=None, updated_time=None, error=None, deployment_type=None, created_by=None, is_default=None, traffic_percentile=None, type=None, image_details=None, image_id=None, image_digest=None, models_property=None, container_resource_requirements=None, max_concurrent_requests_per_container=None, max_queue_wait_ms=None, compute_name=None, namespace=None, num_replicas=None, data_collection=None, app_insights_enabled=None, auto_scaler=None, scoring_uri=None, deployment_status=None, scoring_timeout_ms=None, liveness_probe_requirements=None, auth_enabled=None, aad_auth_enabled=None, swagger_uri=None, model_config_map=None, environment_image_request=None):
        super(AKSServiceResponse, self).__init__(id=id, name=name, description=description, kv_tags=kv_tags, properties=properties, operation_id=operation_id, state=state, created_time=created_time, updated_time=updated_time, error=error, deployment_type=deployment_type, created_by=created_by, is_default=is_default, traffic_percentile=traffic_percentile, type=type)
        self.image_details = image_details
        self.image_id = image_id
        self.image_digest = image_digest
        self.models_property = models_property
        self.container_resource_requirements = container_resource_requirements
        self.max_concurrent_requests_per_container = max_concurrent_requests_per_container
        self.max_queue_wait_ms = max_queue_wait_ms
        self.compute_name = compute_name
        self.namespace = namespace
        self.num_replicas = num_replicas
        self.data_collection = data_collection
        self.app_insights_enabled = app_insights_enabled
        self.auto_scaler = auto_scaler
        self.scoring_uri = scoring_uri
        self.deployment_status = deployment_status
        self.scoring_timeout_ms = scoring_timeout_ms
        self.liveness_probe_requirements = liveness_probe_requirements
        self.auth_enabled = auth_enabled
        self.aad_auth_enabled = aad_auth_enabled
        self.swagger_uri = swagger_uri
        self.model_config_map = model_config_map
        self.environment_image_request = environment_image_request
        self.compute_type = 'AKS'
