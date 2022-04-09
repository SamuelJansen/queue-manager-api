from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod, ConverterStatic

import SubscriptionModel
import SubscriptionDto


@Mapper()
class SubscriptionModelMapper:

    @MapperMethod(requestClass=[[SubscriptionDto.SubscriptionRequestDto]], responseClass=[[SubscriptionModel.SubscriptionModel]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        return modelList


    @MapperMethod(requestClass=[[SubscriptionModel.SubscriptionModel]], responseClass=[[SubscriptionDto.SubscriptionResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList


    @MapperMethod(requestClass=[SubscriptionDto.SubscriptionRequestDto], responseClass=[SubscriptionModel.SubscriptionModel])
    def fromRequestDtoToModel(self, dto, model):
        return model


    @MapperMethod(requestClass=[SubscriptionModel.SubscriptionModel], responseClass=[SubscriptionDto.SubscriptionResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto


    @MapperMethod(requestClass=[SubscriptionModel.SubscriptionModel, SubscriptionDto.SubscriptionRequestDto])
    def overrideModel(self, model, dto):
        model.url = ConverterStatic.getValueOrDefault(dto.url, model.url)
        model.onErrorUrl = ConverterStatic.getValueOrDefault(dto.onErrorUrl, model.onErrorUrl)
        model.maxTries = ConverterStatic.getValueOrDefault(dto.maxTries, model.maxTries)
        model.backOff = ConverterStatic.getValueOrDefault(dto.backOff, model.backOff)
