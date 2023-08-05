# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Recurrence(Model):
    """Recurrence.

    :param frequency: Possible values include: 'Month', 'Week', 'Day', 'Hour',
     'Minute'
    :type frequency: str or ~swagger.models.enum
    :param interval:
    :type interval: int
    :param start_time:
    :type start_time: str
    :param time_zone:
    :type time_zone: str
    :param schedule:
    :type schedule: ~swagger.models.RecurrenceSchedule
    """

    _attribute_map = {
        'frequency': {'key': 'Frequency', 'type': 'str'},
        'interval': {'key': 'Interval', 'type': 'int'},
        'start_time': {'key': 'StartTime', 'type': 'str'},
        'time_zone': {'key': 'TimeZone', 'type': 'str'},
        'schedule': {'key': 'Schedule', 'type': 'RecurrenceSchedule'},
    }

    def __init__(self, frequency=None, interval=None, start_time=None, time_zone=None, schedule=None):
        super(Recurrence, self).__init__()
        self.frequency = frequency
        self.interval = interval
        self.start_time = start_time
        self.time_zone = time_zone
        self.schedule = schedule
