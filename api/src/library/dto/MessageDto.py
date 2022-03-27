class MessageRequestDto:
    def __init__(self,
        key = None,
        queueKey = None,
        content = None
    ):
        self.key = key
        self.queueKey = queueKey
        self.content = content


class MessageResponseDto:
    def __init__(self,
        key = None,
        queueKey = None,
        content = None
    ):
        self.key = key
        self.queueKey = queueKey
        self.content = content
