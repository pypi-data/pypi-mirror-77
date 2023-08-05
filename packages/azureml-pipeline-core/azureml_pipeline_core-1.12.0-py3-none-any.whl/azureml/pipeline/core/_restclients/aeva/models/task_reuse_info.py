# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TaskReuseInfo(Model):
    """TaskReuseInfo.

    :param experiment_id:
    :type experiment_id: str
    :param node_id:
    :type node_id: str
    :param request_id:
    :type request_id: str
    :param run_id:
    :type run_id: str
    :param node_start_time:
    :type node_start_time: datetime
    :param node_end_time:
    :type node_end_time: datetime
    """

    _attribute_map = {
        'experiment_id': {'key': 'ExperimentId', 'type': 'str'},
        'node_id': {'key': 'NodeId', 'type': 'str'},
        'request_id': {'key': 'RequestId', 'type': 'str'},
        'run_id': {'key': 'RunId', 'type': 'str'},
        'node_start_time': {'key': 'NodeStartTime', 'type': 'iso-8601'},
        'node_end_time': {'key': 'NodeEndTime', 'type': 'iso-8601'},
    }

    def __init__(self, experiment_id=None, node_id=None, request_id=None, run_id=None, node_start_time=None, node_end_time=None):
        super(TaskReuseInfo, self).__init__()
        self.experiment_id = experiment_id
        self.node_id = node_id
        self.request_id = request_id
        self.run_id = run_id
        self.node_start_time = node_start_time
        self.node_end_time = node_end_time
