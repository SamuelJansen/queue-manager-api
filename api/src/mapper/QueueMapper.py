from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

import Queue
from dto import QueueDto


@Mapper()
class QueueMapper:

    @MapperMethod(requestClass=[[QueueDto.QueueRequestDto]], responseClass=[[Queue.Queue]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList


    @MapperMethod(requestClass=[[Queue.Queue]], responseClass=[[QueueDto.QueueResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList


    @MapperMethod(requestClass=[QueueDto.QueueRequestDto], responseClass=[Queue.Queue])
    def fromRequestDtoToModel(self, dto, model):
        return model


    @MapperMethod(requestClass=[Queue.Queue], responseClass=[QueueDto.QueueResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto


    @MapperMethod(requestClass=[Queue.Queue, QueueDto.QueueRequestDto])
    def overrideModel(self, model, dto):
        ...
