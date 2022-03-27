from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import MessageDto
import Message


@Validator()
class MessageValidator:

    @ValidatorMethod(requestClass=[MessageDto.MessageRequestDto])
    def validateRequestDto(self, dto):
        if ObjectHelper.isNone(dto) or ObjectHelper.isNone(dto.key):
            raise GlobalException(
                logMessage = f'Message key cannot be None. Message dto: {dto}.',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )


    @ValidatorMethod(requestClass=[MessageDto.MessageRequestDto])
    def validateDoesNotExists(self, dto):
        self.validateRequestDto(dto)
        if self.service.message.existsByKey(dto.key):
            raise GlobalException(
                message = 'Message aleady exists.',
                logMessage = f'Message {dto.key} aleady exists.',
                status = HttpStatus.BAD_REQUEST
            )


    @ValidatorMethod(requestClass=[[Message.Message]])
    def validateAllBelongsToTheSameQueue(self, modelList):
        if not 1 == len({model.queueKey for model in modelList if ObjectHelper.isNotNone(model.queueKey)}):
            raise GlobalException(
                logMessage = f'All messages should be from the same queue. Messages: {modelList}.',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )
