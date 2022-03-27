from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

import GroupDto
import Group

@Validator()
class GroupValidator:

    @ValidatorMethod(requestClass=[GroupDto.GroupRequestDto])
    def validateRequestDto(self, dto):
        if ObjectHelper.isNone(dto) or ObjectHelper.isNone(dto.key):
            raise GlobalException(
                logMessage = f'Group key cannot be None. Group dto: {dto}.',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )


    @ValidatorMethod(requestClass=[GroupDto.GroupRequestDto])
    def validateDoesNotExists(self, dto):
        self.validateRequestDto(dto)
        if self.service.queue.existsByKey(dto.key):
            raise GlobalException(
                message = 'Group aleady exists.',
                logMessage = f'Group {dto.key} aleady exists.',
                status = HttpStatus.BAD_REQUEST
            )


    @ValidatorMethod(requestClass=[[Group.Group], str])
    def validateIsAtLeastOne(self, modelList, queueKey):
        if ObjectHelper.isEmpty(modelList):
            raise GlobalException(
                logMessage = f'There are no groups listenning to this queue: {queueKey}. Groups: {modelList}.',
                status = HttpStatus.BAD_REQUEST
            )


    @ValidatorMethod(requestClass=[[Group.Group]])
    def validateIsExactlyOne(self, modelList):
        if ObjectHelper.isEmpty(modelList):
            raise GlobalException(
                message = 'Group not found.',
                logMessage = f'An empty list of groups was given: {modelList}',
                status = HttpStatus.BAD_REQUEST
            )
        if 1 < len(modelList):
            raise GlobalException(
                logMessage = f'There are more than one group with the same key: {modelList}.',
                status = HttpStatus.INTERNAL_SERVER_ERROR
            )
