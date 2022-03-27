from python_helper import ObjectHelper
from python_framework import Repository


@Repository()
class MemoryRepository:

    messageDictionary = {}


    def existsByQueueKeyAndKey(self, queueKey, key):
        return key in self.getQueue(queueKey)


    def findAllByStateIn(self, stateList):
        return [
            self.getMessage(queueKey, key)
            for queueKey in self.getQueueKeyIterator()
            for key in self.getKeyIterator(queueKey)
            if self.messageStateIn(queueKey, key, stateList)
        ]


    def removeAllByStateIn(self, stateList):
        modelList = [
            self.popMessage(queueKey, key)
            for queueKey in self.getQueueKeyIterator()
            for key in self.getKeyIterator(queueKey)
            if self.messageStateIn(queueKey, key, stateList)
        ]
        self.removeEmptyQueues()
        return modelList


    def findAllByStatusIn(self, statusList):
        return [
            self.getMessage(queueKey, key)
            for queueKey in self.getQueueKeyIterator()
            for key in self.getKeyIterator(queueKey)
            if self.messageStatusIn(queueKey, key, statusList)
        ]


    def removeAllByStatusIn(self, statusList):
        modelList = [
            self.popMessage(queueKey, key)
            for queueKey in self.getQueueKeyIterator()
            for key in self.getKeyIterator(queueKey)
            if self.messageStatusIn(queueKey, key, statusList)
        ]
        self.removeEmptyQueues()
        return modelList


    def findAllByStatusInFromOneQueue(self, statusList):
        queueKeyList = [*self.getQueueKeyIterator()]
        if ObjectHelper.isEmpty(queueKeyList):
            return []
        modelList = []
        for queueKey in queueKeyList:
            modelList = [
                self.getMessage(queueKeyList[0], key) for key in self.getKeyIterator(queueKeyList[0])
                if self.messageStatusIn(queueKeyList[0], key, statusList)
            ]
            if 0 < len(modelList):
                break
            else:
                modelList = []
        return modelList


    def removeEmptyQueues(self):
        for queueKey in self.getQueueKeyIterator():
            if ObjectHelper.isEmpty(self.getQueue(queueKey)):
                ObjectHelper.deleteDictionaryEntry(queueKey)


    def getKeyIterator(self, queueKey):
        return [*self.getQueue(queueKey).keys()]


    def getMessage(self, queueKey, key):
        return self.getQueue(queueKey).get(key)


    def popMessage(self, queueKey, key):
        return self.getQueue(queueKey).pop(key)


    def accept(self, message):
        if message.queueKey not in self.messageDictionary:
            self.messageDictionary[message.queueKey] = {}
        self.messageDictionary[message.queueKey][message.key] = message


    def messageStateIn(self, queueKey, key, stateList):
        return ObjectHelper.isNotNone(self.getMessage(queueKey, key)) and self.getMessage(queueKey, key).state in stateList


    def messageStatusIn(self, queueKey, key, statusList):
        return ObjectHelper.isNotNone(self.getMessage(queueKey, key)) and self.getMessage(queueKey, key).status in statusList


    def getQueueKeyIterator(self):
        return [*{**self.messageDictionary}.keys()]


    def getQueue(self, queueKey):
        return self.messageDictionary.get(queueKey, {})
