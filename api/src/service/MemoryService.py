from python_helper import log
from python_framework import Service, ServiceMethod

import Message
from enumeration.MessageState import MessageState
from enumeration.MessageStatus import MessageStatus


@Service()
class MemoryService:


    @ServiceMethod(requestClass=[Message.Message])
    def accept(self, message):
        self.validator.memory.validateDoesNotExists(message)
        return self.repository.memory.accept(message)


    @ServiceMethod(requestClass=[Message.Message])
    def exists(self, message):
        return self.repository.memory.existsByQueueKeyAndKey(message.queueKey, message.key)


    @ServiceMethod()
    def getAllInstantiated(self):
        return self.repository.memory.findAllByStateIn([MessageState.INSTANTIATED])


    @ServiceMethod()
    def getAllAccepted(self):
        return self.repository.memory.findAllByStatusIn([MessageStatus.ACCEPTED])


    @ServiceMethod()
    def getAllAcceptedFromOneQueue(self):
        return self.repository.memory.findAllByStatusInFromOneQueue([MessageStatus.ACCEPTED])


    @ServiceMethod()
    def removeAllProcessed(self):
        modelList = self.repository.memory.removeAllByStateIn([MessageState.PROCESSED])
        log.prettyPython(self.removeAllProcessed, 'Messages removed from memory', modelList, logLevel=log.DEBUG)
        return modelList
