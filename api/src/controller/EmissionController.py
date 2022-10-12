from python_framework import Controller, ControllerMethod, HttpStatus

from enumeration.AccessDomain import AccessDomain
import EmissionDto


@Controller(
    url = '/emission',
    tag = 'Emission',
    description = 'Emission controller'
    # , logRequest = True
    # , logResponse = True
)
class EmissionAllController:

    @ControllerMethod(url = '/all',
        apiKeyRequired = [AccessDomain.ADMIN],
        requestParamClass = [EmissionDto.EmissionQueryRequestDto],
        responseClass = [[EmissionDto.EmissionQueryResponseDto]]
    )
    def get(self, params=None):
        return self.service.emission.findAllByQuery(params), HttpStatus.OK
