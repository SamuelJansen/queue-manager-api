from python_helper import log
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()
from constant import MessageKeyConfigConstant


EMITTER_TIMEOUT = globalsInstance.getSetting(MessageKeyConfigConstant.EMITTER_TIMEOUT)

LISTENER_URI = globalsInstance.getSetting(MessageKeyConfigConstant.LISTENER_URI)
LISTENER_TIMEOUT = globalsInstance.getSetting(MessageKeyConfigConstant.LISTENER_TIMEOUT)
