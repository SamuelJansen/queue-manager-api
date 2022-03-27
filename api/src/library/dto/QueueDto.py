from python_framework import ConverterStatic


class QueueRequestDto:
    def __init__(self,
        key = None,
        groupList = None
    ):
        self.key = key
        self.groupList = ConverterStatic.getValueOrDefault(groupList, list())


class QueueResponseDto:
    def __init__(self,
        key = None,
        groupList = None
    ):
        self.key = key
        self.groupList = ConverterStatic.getValueOrDefault(groupList, list())
