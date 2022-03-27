from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import QueueDto
from Group import Group

@Validator()
class QueueValidator:

    @ValidatorMethod(requestClass=[QueueDto.QueueRequestDto])
    def validateRequestDto(self, dto):
        if ObjectHelper.isNone(dto) or ObjectHelper.isNone(dto.key):
            raise GlobalException(
                logMessage = f'Queue key cannot be None. Queue dto: {dto}.',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )


    @ValidatorMethod(requestClass=[QueueDto.QueueRequestDto])
    def validateDoesNotExists(self, dto):
        self.validateRequestDto(dto)
        if self.service.queue.existsByKey(dto.key):
            raise GlobalException(
                message = 'Queue aleady exists.',
                logMessage = f'Queue {dto.key} aleady exists.',
                status = HttpStatus.BAD_REQUEST
            )
