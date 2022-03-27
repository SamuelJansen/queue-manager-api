from ModelAssociation import MESSAGE


class Message:
    __tablename__ = MESSAGE

    def __init__(self,
        id = None,
        key = None,
        queueKey = None,
        status = None,
        statusMessage = None,
        content = None,
        state = None
    ):
        self.id = id
        self.key = key
        self.queueKey = queueKey
        self.status = status
        self.statusMessage = statusMessage
        self.content = content
        self.state = state

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, queueKey={self.queueKey}, status={self.status}, state={self.state})'
