# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EntityWithContinuationTokenIEnumerablePipelineScheduleEntity(Model):
    """EntityWithContinuationTokenIEnumerablePipelineScheduleEntity.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar entity:
    :vartype entity: list[~swagger.models.PipelineScheduleEntity]
    :ivar continuation_token:
    :vartype continuation_token: str
    """

    _validation = {
        'entity': {'readonly': True},
        'continuation_token': {'readonly': True},
    }

    _attribute_map = {
        'entity': {'key': 'Entity', 'type': '[PipelineScheduleEntity]'},
        'continuation_token': {'key': 'ContinuationToken', 'type': 'str'},
    }

    def __init__(self):
        super(EntityWithContinuationTokenIEnumerablePipelineScheduleEntity, self).__init__()
        self.entity = None
        self.continuation_token = None
