from python_framework import Controller, ControllerMethod, HttpStatus

from enumeration.AccessDomain import AccessDomain
import MessageDto


@Controller(url = '/api/message/emitter', tag='Message', description='Message controller')
class MessageController:

    @ControllerMethod(url = '/',
        apiKeyRequired = [AccessDomain.API, AccessDomain.USER],
        requestClass = [MessageDto.MessageRequestDto]
        # responseClass = [MessageDto.MessageResponseDto]
        # responseClass = [MessageDto.MessageRequestDto]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self, dto):
        return self.service.message.acceptWithoutValidation(dto), HttpStatus.ACCEPTED
