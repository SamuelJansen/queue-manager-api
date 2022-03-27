from python_framework import Controller, ControllerMethod, HttpStatus

from enumeration.QueueDomain import QueueDomain
from dto import QueueDto


@Controller(url = '/queue', tag='Queue', description='Queue controller')
class QueueController:

    @ControllerMethod(url = '/',
        # apiKey = [QueueDomain.API],
        requestClass = [QueueDto.QueueRequestDto],
        responseClass = [QueueDto.QueueResponseDto]
        , logRequest = True
        , logResponse = True
    )
    def post(self, dto):
        # return self.service.queue.createOrUpdate(dto), HttpStatus.CREATED
        return dto, HttpStatus.CREATED
