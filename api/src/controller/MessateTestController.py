from python_framework import Controller, ControllerMethod, HttpStatus, ConverterStatic

from enumeration.AccessDomain import AccessDomain
import MessageDto


@Controller(
    url = '/test/message',
    tag = 'QueueTest',
    description = 'Queue test controller'
    , logRequest = True
    , logResponse = True
)
class MessateTestController:


    @ControllerMethod(url = '/',
        apiKeyRequired = ['SOMETHING_ELSE'],
        requestClass = [MessageDto.MessageRequestDto],
        responseClass = [MessageDto.MessageResponseDto]
    )
    def post(self, dto):
        return ConverterStatic.to(dto, MessageDto.MessageResponseDto), HttpStatus.OK


@Controller(
    url = '/test/message-error',
    tag = 'QueueTest',
    description = 'Queue test controller'
    , logRequest = True
    , logResponse = True
)
class MessateTestBulkController:

    @ControllerMethod(url = '/',
        apiKeyRequired = [AccessDomain.API],
        requestClass = [MessageDto.MessageRequestDto],
        responseClass = [MessageDto.MessageResponseDto]
    )
    def post(self, dto):
        return ConverterStatic.to(dto, MessageDto.MessageResponseDto), HttpStatus.OK
