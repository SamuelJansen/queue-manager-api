import requests
from python_helper import Constant as c
from python_helper import ReflectionHelper, ObjectHelper, log, Function, StringHelper
from python_framework import (
    FlaskManager,
    ConverterStatic,
    Emitter,
    EmitterMethod,
    FlaskUtil,
    ClientUtil,
    LogConstant,
    OpenApiManager,
    ConfigurationKeyConstant,
    HttpDomain,
    Serializer,
    GlobalException
)

try:
    from queue_manager_api.api.src.library.util import AnnotationUtil
    from queue_manager_api.api.src.library.dto import MessageDto
    from queue_manager_api.api.src.library.constant import HttpEmitterConstant
    from queue_manager_api.api.src.library.constant import MessageConstant
    from queue_manager_api.api.src.library.util import ThreadUtil
except:
    import AnnotationUtil, ThreadUtil
    import HttpEmitterConstant, MessageConstant
    import MessageDto


DEFAULT_TIMEOUT = 2


@Function
def MessageEmitter(
    *resourceArgs,
    url = c.SLASH,
    headers = None,
    timeout = DEFAULT_TIMEOUT,
    logRequest = False,
    logResponse = False,
    enabled = None,
    muteLogs = None,
    eventContext = HttpDomain.EMITTER_CONTEXT,
    **resourceKwargs
):
    def Wrapper(OuterClass, *outterArgs, **outterKwargs):
        resourceUrl = url
        resourceHeaders = ConverterStatic.getValueOrDefault(headers, dict())
        resourceTimeout = timeout
        resourceEventContext = eventContext
        resourceLogRequest = logRequest
        resourceLogResponse = logResponse
        resourceEnabled = enabled
        resourceMuteLogs = muteLogs
        log.wrapper(MessageEmitter, f'''wrapping {OuterClass.__name__}(*{outterArgs}, **{outterKwargs})''')
        api = FlaskManager.getApi()
        class InnerClass(OuterClass):
            url = resourceUrl
            headers = resourceHeaders
            def __init__(self, *args, **kwargs):
                log.wrapper(OuterClass, f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self, *args,**kwargs)
                AnnotationUtil.initializeComunicationLayerResource(
                    resourceInstance = self,
                    api = api,
                    timeout = resourceTimeout,
                    enabled = resourceEnabled,
                    muteLogs = resourceMuteLogs,
                    logRequest = resourceLogRequest,
                    logResponse = resourceLogResponse,
                    resourceEnabledConfigKey = ConfigurationKeyConstant.API_EMITTER_ENABLE,
                    resourceMuteLogsConfigKey = ConfigurationKeyConstant.API_EMITTER_MUTE_LOGS,
                    resourceTimeoutConfigKey = ConfigurationKeyConstant.API_EMITTER_TIMEOUT
                )
                self.threadManager = ThreadUtil.ThreadManager(threadTimeout=self.timeout)
            def emit(self, *args, **kwargs):
                raise ClientUtil.HttpClientEvent(HttpDomain.Verb.POST, *args, eventContext=resourceEventContext, **kwargs)
        ReflectionHelper.overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper


class EmitterMethodConfig:
    def __init__(self,
        url = None,
        headers = None,
        requestHeaderClass = None,
        requestParamClass = None,
        requestClass = None,
        responseClass = None,
        returnOnlyBody = None,
        timeout = DEFAULT_TIMEOUT,
        propagateAuthorization = None,
        propagateApiKey = None,
        propagateSession = None,
        produces = None,
        consumes = None,
        logRequest = None,
        logResponse = None,
        enabled = None,
        muteLogs = None
    ):
        self.url = url
        self.headers = headers
        self.requestHeaderClass = requestHeaderClass
        self.requestParamClass = requestParamClass
        self.requestClass = requestClass
        self.responseClass = responseClass
        self.returnOnlyBody = returnOnlyBody
        self.timeout = timeout
        self.propagateAuthorization = propagateAuthorization
        self.propagateApiKey = propagateApiKey
        self.propagateSession = propagateSession
        self.produces = produces
        self.consumes = consumes
        self.logRequest = logRequest
        self.logResponse = logResponse
        self.enabled = enabled
        self.muteLogs = muteLogs


@Function
def MessageEmitterMethod(
    *methodArgs,
    url = c.BLANK,
    headers = None,
    requestHeaderClass = None,
    requestParamClass = None,
    requestClass = None,
    responseClass = None,
    returnOnlyBody = True,
    timeout = None,
    consumes = OpenApiManager.DEFAULT_CONTENT_TYPE,
    produces = OpenApiManager.DEFAULT_CONTENT_TYPE,
    logRequest = True,
    logResponse = True,
    enabled = True,
    muteLogs = False,
    debugIt = False,
    muteStacktraceOnBusinessRuleException = True,
    queueKey = None,
    **methodKwargs
):
    resourceMethodConfig = EmitterMethodConfig(
        url = url,
        headers = headers,
        requestHeaderClass = requestHeaderClass,
        requestParamClass = requestParamClass,
        requestClass = requestClass,
        responseClass = responseClass,
        returnOnlyBody = returnOnlyBody,
        timeout = timeout,
        propagateAuthorization = False,
        propagateApiKey = False,
        propagateSession = False,
        produces = produces,
        consumes = consumes,
        logRequest = logRequest,
        logResponse = logResponse,
        enabled = enabled,
        muteLogs = muteLogs
    )
    def innerMethodWrapper(resourceInstanceMethod, *innerMethodArgs, **innerMethodKwargs) :
        wrapperManager = AnnotationUtil.InnerMethodWrapperManager(
            wrapperType = MessageEmitterMethod,
            resourceInstanceMethod = resourceInstanceMethod,
            timeout = timeout,
            enabled = enabled,
            muteLogs = muteLogs,
            logRequest = logRequest,
            logResponse = logResponse,
            resourceTypeName = FlaskManager.KW_EMITTER_RESOURCE,
            resourceEnabledConfigKey = ConfigurationKeyConstant.API_EMITTER_ENABLE,
            resourceMuteLogsConfigKey = ConfigurationKeyConstant.API_EMITTER_MUTE_LOGS,
            resourceTimeoutConfigKey = ConfigurationKeyConstant.API_EMITTER_TIMEOUT
        )
        resourceMethodQueueKey = queueKey
        resourceMethodConfig.wrapperManager = wrapperManager
        def post(
            resourceInstance,
            body = None,
            url = None,
            headers = None,
            params = None,
            timeout = None,
            logRequest = False,
            messageKey = None,
            queueKey = resourceMethodQueueKey,
            groupKey = None,
            **kwargs
        ):
            verb = HttpDomain.Verb.POST
            url, params, headers, body, timeout, logRequest = ClientUtil.parseParameters(
                resourceInstance,
                resourceMethodConfig,
                url,
                params,
                headers,
                Serializer.getObjectAsDictionary(
                    MessageDto.MessageRequestDto(
                        key = ConverterStatic.getValueOrDefault(messageKey, Serializer.newUuid()),
                        queueKey = queueKey,
                        groupKey = groupKey,
                        content = body
                    )
                ),
                timeout,
                logRequest and resourceMethodConfig.wrapperManager.logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest, kwargs)
            emitterMethodResponse = requests.post(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return emitterMethodResponse

        def doLogRequest(verb, url, body, params, headers, logRequest, requestKwargs):
            log.info(resourceInstanceMethod, f'{LogConstant.EMITTER_SPACE}{verb}{c.SPACE_DASH_SPACE}{url}')
            if logRequest:
                parsetRequestKwargs = {} if ObjectHelper.isEmpty(requestKwargs) else {'requestKwargs': {**requestKwargs}}
                log.prettyJson(
                    resourceInstanceMethod,
                    LogConstant.EMITTER_REQUEST,
                    {
                        'headers': ConverterStatic.getValueOrDefault(headers, dict()),
                        'query': ConverterStatic.getValueOrDefault(params, dict()),
                        'body': ConverterStatic.getValueOrDefault(body, dict()),
                        **parsetRequestKwargs
                    },
                    condition = True,
                    logLevel = log.INFO
                )

        HTTP_CLIENT_RESOLVERS_MAP = {
            HttpDomain.Verb.POST : post
        }
        def innerResourceInstanceMethod(*args, **kwargs):
            f'''(*args, {FlaskUtil.KW_HEADERS}={{}}, {FlaskUtil.KW_PARAMETERS}={{}}, **kwargs)'''
            wrapperManager.updateResourceInstance(args)
            httpClientResolversMap = HTTP_CLIENT_RESOLVERS_MAP
            resourceMethodGroupKey = None if MessageConstant.GROUP_KEY_CLIENT_ATTRIBUTE_NAME not in kwargs else kwargs.pop(MessageConstant.GROUP_KEY_CLIENT_ATTRIBUTE_NAME)
            resourceMethodMessageKey = None if MessageConstant.MESSAGE_KEY_CLIENT_ATTRIBUTE_NAME not in kwargs else kwargs.pop(MessageConstant.MESSAGE_KEY_CLIENT_ATTRIBUTE_NAME)
            key = ConverterStatic.getValueOrDefault(resourceMethodMessageKey, Serializer.newUuid())
            messageCreationRequest = MessageDto.MessageCreationRequestDto(
                key = key,
                queueKey = resourceMethodQueueKey,
                groupKey = ConverterStatic.getValueOrDefault(resourceMethodGroupKey, key)
            )
            wrapperManager.resourceInstance.threadManager.runInAThread(
                resolveClientCall,
                args,
                kwargs,
                wrapperManager,
                requestClass,
                requestHeaderClass,
                requestParamClass,
                httpClientResolversMap,
                messageCreationRequest.groupKey,
                messageCreationRequest.key
            )
            return messageCreationRequest
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, wrapperManager.resourceInstanceMethod)
        innerResourceInstanceMethod.url = resourceMethodConfig.url
        innerResourceInstanceMethod.headers = resourceMethodConfig.headers
        innerResourceInstanceMethod.requestHeaderClass = resourceMethodConfig.requestHeaderClass
        innerResourceInstanceMethod.requestParamClass = resourceMethodConfig.requestParamClass
        innerResourceInstanceMethod.requestClass = resourceMethodConfig.requestClass
        innerResourceInstanceMethod.responseClass = resourceMethodConfig.responseClass
        innerResourceInstanceMethod.returnOnlyBody = resourceMethodConfig.returnOnlyBody
        innerResourceInstanceMethod.timeout = resourceMethodConfig.timeout
        innerResourceInstanceMethod.propagateAuthorization = resourceMethodConfig.propagateAuthorization
        innerResourceInstanceMethod.propagateApiKey = resourceMethodConfig.propagateApiKey
        innerResourceInstanceMethod.propagateSession = resourceMethodConfig.propagateSession
        innerResourceInstanceMethod.produces = resourceMethodConfig.produces
        innerResourceInstanceMethod.consumes = resourceMethodConfig.consumes
        innerResourceInstanceMethod.logRequest = resourceMethodConfig.logRequest
        innerResourceInstanceMethod.logResponse = resourceMethodConfig.logResponse
        innerResourceInstanceMethod.enabled = resourceMethodConfig.enabled
        innerResourceInstanceMethod.muteLogs = resourceMethodConfig.muteLogs
        return innerResourceInstanceMethod
    return innerMethodWrapper


def resolveClientCall(
    args,
    kwargs,
    wrapperManager,
    requestClass,
    requestHeaderClass,
    requestParamClass,
    httpClientResolversMap,
    resourceMethodGroupKey,
    resourceMethodMessageKey
):
    resourceMethodResponse = None
    completeResponse = None
    try :
        FlaskManager.validateKwargs(
            kwargs,
            wrapperManager.resourceInstance,
            wrapperManager.resourceInstanceMethod,
            requestHeaderClass,
            requestParamClass
        )
        FlaskManager.validateArgs(args, requestClass, wrapperManager.resourceInstanceMethod)
        emitterEvent = ClientUtil.getHttpClientEvent(wrapperManager.resourceInstanceMethod, *args, **kwargs)
        if isinstance(emitterEvent, ClientUtil.ManualHttpClientEvent):
            completeResponse = emitterEvent.completeResponse
        elif isinstance(emitterEvent, ClientUtil.HttpClientEvent):
            try :
                resourceMethodResponse = httpClientResolversMap.get(
                    emitterEvent.verb,
                    ClientUtil.raiseHttpClientEventNotFoundException
                )(
                    wrapperManager.resourceInstance,
                    *emitterEvent.args,
                    groupKey = resourceMethodGroupKey,
                    messageKey = resourceMethodMessageKey,
                    **emitterEvent.kwargs
                )
            except Exception as exception:
                ClientUtil.raiseException(
                    resourceMethodResponse,
                    exception,
                    context = HttpDomain.EMITTER_CONTEXT,
                    businessLogMessage = HttpEmitterConstant.ERROR_AT_CLIENT_CALL_MESSAGE,
                    defaultLogMessage = HttpEmitterConstant.CLIENT_DID_NOT_SENT_ANY_MESSAGE
                )
            ClientUtil.raiseExceptionIfNeeded(
                resourceMethodResponse,
                context = HttpDomain.EMITTER_CONTEXT,
                businessLogMessage = HttpEmitterConstant.ERROR_AT_CLIENT_CALL_MESSAGE,
                defaultLogMessage = HttpEmitterConstant.CLIENT_DID_NOT_SENT_ANY_MESSAGE
            )
            completeResponse = ClientUtil.getCompleteResponse(resourceMethodResponse, responseClass, produces)
            FlaskManager.validateCompleteResponse(responseClass, completeResponse)
        else:
            raise Exception('Unknown emitter event')
    except Exception as exception:
        if isinstance(exception, GlobalException):
            log.log(resolveClientCall, 'Failure at emitter method execution', exception=exception, muteStackTrace=True)
        else:
            log.failure(resolveClientCall, 'Failure at emitter method execution', exception=exception)
        FlaskManager.raiseAndPersistGlobalException(
            exception,
            wrapperManager.resourceInstance,
            wrapperManager.resourceInstanceMethod,
            context = HttpDomain.EMITTER_CONTEXT
        )
    resourceMethodResponseStatus = completeResponse[-1]
    resourceMethodResponseHeaders = completeResponse[1]
    resourceMethodResponseBody = completeResponse[0] if ObjectHelper.isNotNone(completeResponse[0]) else {'message' : HttpStatus.map(resourceMethodResponseStatus).enumName}
    if wrapperManager.shouldLogResponse():
        log.prettyJson(
            wrapperManager.resourceInstanceMethod,
            LogConstant.EMITTER_RESPONSE,
            {
                'headers': resourceMethodResponseHeaders,
                'body': Serializer.getObjectAsDictionary(resourceMethodResponseBody, muteLogs=not debugIt),
                'status': resourceMethodResponseStatus
            },
            condition = True,
            logLevel = log.INFO
        )
    if returnOnlyBody:
        return completeResponse[0]
    else:
        return completeResponse
