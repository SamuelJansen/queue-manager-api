from python_framework import Controller, ControllerMethod, HttpStatus

from enumeration.QueueDomain import QueueDomain
from dto import MessageDto


@Controller(url = '/message-test', tag='Queue', description='Queue controller')
class MessateTestController:

    @ControllerMethod(url = '/',
        # apiKey = [QueueDomain.API],
        requestClass = [MessageDto.MessageRequestDto],
        # responseClass = [MessageDto.MessageResponseDto]
        responseClass = [MessageDto.MessageRequestDto]
        , logRequest = True
        , logResponse = True
    )
    def post(self, dto):
        return dto, HttpStatus.OK
