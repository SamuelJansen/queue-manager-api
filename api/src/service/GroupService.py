from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod

from dto import QueueDto
import Queue


@Service()
class GroupService:

    @ServiceMethod(requestClass=[str])
    def findAllModelByQueueKey(self, queueKey):
        modelList = self.repository.queue.findAllByQueueKey(queueKey)
        self.validator.queue.validateIsAtLeastOne(modelList, queueKey)
        return modelList


    @ServiceMethod(requestClass=[[str]])
    def findAllModelByQueueKeyIn(self, queueKeyList):
        raise Exception('You should never make such a question')


    @ServiceMethod(requestClass=[str])
    def existsByKey(self, key):
        return self.repository.message.existsByKey(key)


    @ServiceMethod(requestClass=[str])
    def findModelByKey(self, key):
        modelList = self.repository.group.findAllByKey(key)
        self.validator.queue.validateIsExactlyOne(modelList)
        return modelList[0]
