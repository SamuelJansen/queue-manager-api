from python_helper import Constant as c
from python_helper import ObjectHelper, StringHelper
from python_framework import Mapper, MapperMethod, EnumItem

import Message
from dto import MessageDto
from enumeration.MessageState import MessageState


@Mapper()
class MessageMapper:

    @MapperMethod(requestClass=[[MessageDto.MessageRequestDto]], responseClass=[[Message.Message]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        self.overrideAllModelState(modelList, MessageState.INSTANTIATED)
        return modelList


    @MapperMethod(requestClass=[[Message.Message]], responseClass=[[MessageDto.MessageResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList


    @MapperMethod(requestClass=[MessageDto.MessageRequestDto], responseClass=[Message.Message])
    def fromRequestDtoToModel(self, dto, model):
        self.overrideModelState(model, MessageState.INSTANTIATED)
        return model


    @MapperMethod(requestClass=[Message.Message], responseClass=[MessageDto.MessageResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto


    @MapperMethod(requestClass=[Message.Message, EnumItem])
    def overrideModelState(self, model, state):
        model.state = state


    @MapperMethod(requestClass=[[Message.Message], EnumItem])
    def overrideAllModelState(self, modelList, state):
        for model in modelList:
            self.overrideModelState(model, state)


    @MapperMethod(requestClass=[Message.Message, EnumItem])
    def overrideModelStatus(self, model, status, statusMessage=c.BLANK):
        model.status = status
        if StringHelper.isNotBlank(statusMessage):
            model.statusMessage = statusMessage


    @MapperMethod(requestClass=[[Message.Message], EnumItem])
    def overrideAllModelStatus(self, modelList, status, statusMessage=c.BLANK):
        for model in modelList:
            self.overrideModelStatus(model, status, statusMessage=statusMessage)
