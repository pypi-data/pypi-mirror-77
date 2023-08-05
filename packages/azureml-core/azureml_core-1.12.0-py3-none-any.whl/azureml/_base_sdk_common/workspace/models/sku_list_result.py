# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SkuListResult(Model):
    """List of skus with features.

    :param value:
    :type value: list[~machinelearningservices.models.WorkspaceSku]
    :param next_link: The URI to fetch the next page of Workspace Skus. Call
     ListNext() with this URI to fetch the next page of Workspace Skus
    :type next_link: str
    """

    _attribute_map = {
        'value': {'key': 'value', 'type': '[WorkspaceSku]'},
        'next_link': {'key': 'nextLink', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(SkuListResult, self).__init__(**kwargs)
        self.value = kwargs.get('value', None)
        self.next_link = kwargs.get('next_link', None)
