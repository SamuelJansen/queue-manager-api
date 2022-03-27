from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod

from dto import QueueDto
import Queue


@Service()
class QueueService:

    @ServiceMethod(requestClass=[QueueDto.QueueRequestDto])
    def createOrUpdate(self, dto):
        self.validator.queue.validateRequestDto(dto)
        model = self.findByKey(dto.key)
        if ObjectHelper.isNotNone(model):
            self.mapper.queue.overrideModel(model, dto)
        else:
            model = self.mapper.queue.fromRequestDtoToModel(dto)
        return self.mapper.queue.fromModelToResponseDto(self.persist(model))


    @ServiceMethod(requestClass=[str])
    def findByKey(self, key):
        return self.repository.queue.findByKey(key)


    @ServiceMethod(requestClass=[Queue.Queue])
    def persist(self, model):
        return self.repository.queue.save(model)
