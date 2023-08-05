# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WorkspaceSku(Model):
    """Describes Workspace Sku details and features.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar locations: The set of locations that the SKU is available. This will
     be supported and registered Azure Geo Regions (e.g. West US, East US,
     Southeast Asia, etc.).
    :vartype locations: list[str]
    :ivar location_info: A list of locations and availability zones in those
     locations where the SKU is available.
    :vartype location_info:
     list[~machinelearningservices.models.ResourceSkuLocationInfo]
    :ivar tier: Sku Tier like Basic or Enterprise
    :vartype tier: str
    :ivar resource_type:
    :vartype resource_type: str
    :ivar name:
    :vartype name: str
    :ivar capabilities: List of features/user capabilities associated with the
     sku
    :vartype capabilities: list[~machinelearningservices.models.SKUCapability]
    :param restrictions: The restrictions because of which SKU cannot be used.
     This is empty if there are no restrictions.
    :type restrictions: list[~machinelearningservices.models.Restriction]
    """

    _validation = {
        'locations': {'readonly': True},
        'location_info': {'readonly': True},
        'tier': {'readonly': True},
        'resource_type': {'readonly': True},
        'name': {'readonly': True},
        'capabilities': {'readonly': True},
    }

    _attribute_map = {
        'locations': {'key': 'locations', 'type': '[str]'},
        'location_info': {'key': 'locationInfo', 'type': '[ResourceSkuLocationInfo]'},
        'tier': {'key': 'tier', 'type': 'str'},
        'resource_type': {'key': 'resourceType', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'capabilities': {'key': 'capabilities', 'type': '[SKUCapability]'},
        'restrictions': {'key': 'restrictions', 'type': '[Restriction]'},
    }

    def __init__(self, **kwargs):
        super(WorkspaceSku, self).__init__(**kwargs)
        self.locations = None
        self.location_info = None
        self.tier = None
        self.resource_type = None
        self.name = None
        self.capabilities = None
        self.restrictions = kwargs.get('restrictions', None)
