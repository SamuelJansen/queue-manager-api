from python_helper import ObjectHelper
from python_framework import Repository

import MessageModel


@Repository(model = MessageModel.MessageModel)
class MessageModelRepository:

    def save(self, model) :
        return self.repository.saveAndCommit(model)

    def saveAll(self, modelList):
        return self.repository.saveAllAndCommit(modelList)

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def findByKey(self, key) :
        if self.existsByKey(key) :
            return self.repository.findByKeyAndCommit(key, self.model)

    def findAllByKeyIn(self, keyList) :
        modelList = self.repository.session.query(self.model).filter(self.model.key.in_(keyList)).all()
        self.repository.session.commit()
        return modelList

    def findById(self, id) :
        if self.existsById(id) :
            return self.repository.findByIdAndCommit(id, self.model)

    def findAllByIdIn(self, idList) :
        modelList = self.repository.session.query(self.model).filter(self.model.id.in_(idList)).all()
        self.repository.session.commit()
        return modelList

    def findAllByQuery(self, query):
        modelList = self.repository.session.query(self.model).filter_by(
            **{
                k: v
                for k, v in query.items()
                if ObjectHelper.isNotNone(v)
            }
        ).all()
        self.repository.session.commit()
        return self.repository.load(modelList)

    def existsByKey(self, key) :
        return self.repository.existsByKeyAndCommit(key, self.model)

    def notExistsByKey(self, key) :
        return not self.existsByKey(key)

    def existsById(self, id) :
        return self.repository.existsByIdAndCommit(id, self.model)

    def notExistsById(self, id) :
        return not self.existsById(id)

    def deleteByKey(self, key):
        self.repository.deleteByKeyAndCommit(key, self.model)

    def deleteById(self, id):
        self.repository.deleteByIdAndCommit(id, self.model)
