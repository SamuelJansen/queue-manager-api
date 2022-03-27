from python_helper import log, ObjectHelper
from python_framework import Service, ServiceMethod

from dto import MessageDto
import Message
from enumeration.MessageStatus import MessageStatus
from enumeration.MessageState import MessageState


@Service()
class MessageService:

    @ServiceMethod(requestClass=[Message.Message, str])
    def send(self, model, destinyUri):
        return self.emitter.message.send(model, destinyUri)


    @ServiceMethod(requestClass=[MessageDto.MessageRequestDto])
    def acceptWithoutValidation(self, dto):
        model = self.mapper.message.fromRequestDtoToModel(dto)
        self.mapper.message.overrideModelStatus(model, MessageStatus.ACCEPTED)
        log.prettyPython(self.acceptWithoutValidation, f'Accepting new message', model, logLevel=log.STATUS)
        return self.service.memory.accept(model)


    @ServiceMethod()
    def sendMessageListFromOneQueue(self):
        modelList = self.service.memory.getAllAcceptedFromOneQueue()
        self.mapper.message.overrideAllModelStatus(modelList, MessageStatus.SENDING)
        try:
            if ObjectHelper.isEmpty(modelList):
                return modelList
            self.validator.message.validateAllBelongsToTheSameQueue(modelList)
            queue = self.service.queue.findModelByKey(modelList[0].queueKey)
            log.prettyPython(self.sendMessageListFromOneQueue, f'Sending {MessageStatus.ACCEPTED} messages to {queue.key} queue', modelList, logLevel=log.STATUS)
        except Exception as exception:
            self.mapper.message.overrideAllModelStatus(modelList, MessageStatus.ERROR_AT_SENDING, statusMessage=str(exception))
            raise exception


    @ServiceMethod()
    def createAllInstantiatedFromMemory(self):
        modelList = self.service.memory.getAllInstantiated()
        self.mapper.message.overrideAllModelState(modelList, MessageState.PERSISTED)
        return self.service.message.saveAll(modelList)


    @ServiceMethod(requestClass=[[Message.Message]])
    def saveAll(self, modelList):
        ...
        # return self.repository.message.saveAll(modelList)


    @ServiceMethod(requestClass=[str])
    def existsByKey(self, key):
        return self.repository.message.existsByKey(key)
