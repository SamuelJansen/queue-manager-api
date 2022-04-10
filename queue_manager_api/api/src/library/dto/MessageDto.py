class MessageRequestDto:
    def __init__(self,
        key = None,
        queueKey = None,
        groupKey = None,
        content = None
    ):
        self.key = key
        self.queueKey = queueKey
        self.groupKey = groupKey
        self.content = content


class MessageResponseDto:
    def __init__(self,
        key = None,
        queueKey = None,
        groupKey = None,
        content = None,
        history = None
    ):
        self.key = key
        self.queueKey = queueKey
        self.groupKey = groupKey
        self.content = content
        self.history = history

class MessageCreationRequestDto:
    def __init__(self,
        key = None,
        queueKey = None,
        groupKey = None
    ):
        self.key = key
        self.queueKey = queueKey
        self.groupKey = groupKey
