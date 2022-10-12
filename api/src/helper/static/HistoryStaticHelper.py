from python_helper import Constant as c
from python_helper import ObjectHelper, log
from python_framework import StaticConverter, Serializer

DOUBLE_QUOTE_COMA_DOUBLE_QUOTE = '", "'
DOUBLE_QUOTE_COMA_DOUBLE_QUOTE_WITH_BARS = '\", \"'



def addMemoryHistory(memory, history):
    if ObjectHelper.isNeitherNoneNorBlank(history):
        memory.history.append(str(history))


def overrideMemoryHistory(memory, history):
    if ObjectHelper.isNone(history):
        memory.history = []
    elif ObjectHelper.isNotList(history):
        try:
            if isinstance(history, str):
                if ObjectHelper.isNoneOrBlank(history):
                    parsedHistory = []
                else:
                    parsedHistory = Serializer.convertFromJsonToDictionary(history)
            else:
                parsedHistory = Serializer.getObjectAsDictionary(history)
        except Exception as exception:
            parsedHistory = [str(history)]
            log.warning(overrideMemoryHistory, 'Error while parsing history. Setting it as string by default', exception=exception)
        if ObjectHelper.isList(history):
            memory.history = parsedHistory
        else:
            parsedHistoryAsString = str(parsedHistory)
            if ObjectHelper.isNoneOrBlank(parsedHistoryAsString):
                memory.history = []
            else:
                parsedHistoryAsString = parsedHistoryAsString.replace(
                    DOUBLE_QUOTE_COMA_DOUBLE_QUOTE_WITH_BARS,
                    DOUBLE_QUOTE_COMA_DOUBLE_QUOTE
                )
                if not parsedHistoryAsString.startswith(c.OPEN_LIST):
                    if ObjectHelper.isNoneOrBlank(parsedHistoryAsString):
                        memory.history = []
                    else:
                        memory.history = [parsedHistoryAsString]
                else:
                    parsedHistoryAsString = parsedHistoryAsString[1:]
                    if parsedHistoryAsString.endswith(c.CLOSE_LIST):
                        parsedHistoryAsString = parsedHistoryAsString[:-1]
                    if parsedHistoryAsString.startswith(c.SINGLE_QUOTE):
                        parsedHistoryAsString = parsedHistoryAsString[1:]
                    if parsedHistoryAsString.endswith(c.SINGLE_QUOTE):
                        parsedHistoryAsString = parsedHistoryAsString[:-1]
                    if parsedHistoryAsString.startswith(c.DOUBLE_QUOTE):
                        parsedHistoryAsString = parsedHistoryAsString[1:]
                    if parsedHistoryAsString.endswith(c.DOUBLE_QUOTE):
                        parsedHistoryAsString = parsedHistoryAsString[:-1]
                    if ObjectHelper.isNoneOrBlank(parsedHistoryAsString):
                        memory.history = []
                    else:
                        if DOUBLE_QUOTE_COMA_DOUBLE_QUOTE in parsedHistoryAsString:
                            memory.history = parsedHistoryAsString.split(DOUBLE_QUOTE_COMA_DOUBLE_QUOTE)
                        else:
                            memory.history = [parsedHistoryAsString]
    else:
        memory.history = [
            str(h) for h in StaticConverter.getValueOrDefault(history, [])
        ]


def overrideModelHistory(model, history):
    if ObjectHelper.isNeitherNoneNorBlank(history):
        try:
            parsedHistory = Serializer.getObjectAsDictionary(history)
            model.history = Serializer.jsonifyIt(parsedHistory)
        except Exception as exception:
            log.warning(overrideModelHistory, 'Not possible to set histry. Setting it as string by default', exception=exception)
            model.history = Serializer.jsonifyIt([str(history)])
    else:
        model.history = Serializer.jsonifyIt([])


def addModelHistory(model, history):
    if ObjectHelper.isNeitherNoneNorBlank(history):
        try:
            parsedHistory = Serializer.getObjectAsDictionary(history)
            parsedOriginalHistory = StaticConverter.getValueOrDefault(Serializer.convertFromJsonToDictionary(model.history), [])
            parsedOriginalHistory.append(parsedHistory)
            model.history = Serializer.jsonifyIt(parsedOriginalHistory)
        except Exception as exception:
            log.warning(addModelHistory, 'Not possible to set histry. Setting it as string by default', exception=exception)
            model.history = Serializer.jsonifyIt([str(history)])
