from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import Message


@Validator()
class MemoryValidator:

    @ValidatorMethod(requestClass=[Message.Message])
    def validateModel(self, message):
        if ObjectHelper.isNone(message) or ObjectHelper.isNone(message.key) or ObjectHelper.isNone(message.queueKey):
            raise GlobalException(
                logMessage = f'Message key cannot be None. Message: {message}.',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )


    @ValidatorMethod(requestClass=[Message.Message])
    def validateDoesNotExists(self, message):
        self.validateModel(message)
        if self.service.memory.exists(message):
            raise GlobalException(
                message = 'Message aleady in process.',
                logMessage = f'Message "{message.key}" from group "{message.queueKey}" aleady in process.',
                status = HttpStatus.BAD_REQUEST
            )
