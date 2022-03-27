class Queue:
    def __init__(self,
        key = None,
        groupList = None
    ):
        self.key = key
        self.groupList = ConverterStatic.getValueOrDefault(groupList, list())
