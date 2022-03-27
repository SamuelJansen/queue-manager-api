from python_framework import ConverterStatic


class GroupRequestDto:
    def __init__(self,
        key = None,
        listenerUrl = None,
        listenerOnErrorUrl = None,
        retries = None,
        queueList = None
    ):
        self.key = key
        self.listenerUrl = listenerUrl
        self.listenerOnErrorUrl = listenerOnErrorUrl
        self.retries = retries
        self.queueList = ConverterStatic.getValueOrDefault(queueList, list())


class GroupResponseDto:
    def __init__(self,
        key = None,
        listenerUrl = None,
        listenerOnErrorUrl = None,
        retries = None,
        queueList = None
    ):
        self.key = key
        self.listenerUrl = listenerUrl
        self.listenerOnErrorUrl = listenerOnErrorUrl
        self.retries = retries
        self.queueList = ConverterStatic.getValueOrDefault(queueList, list())
