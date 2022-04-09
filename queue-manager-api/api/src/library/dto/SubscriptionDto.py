from python_framework import ConverterStatic

from constant import SubscriptionConstant


class SubscriptionRequestDto:
    def __init__(self,
        key = None,
        url = None,
        onErrorUrl = None,
        maxTries = None,
        backOff = None,
        queue = None
    ):
        self.key = key
        self.url = url
        self.onErrorUrl = onErrorUrl
        self.maxTries = ConverterStatic.getValueOrDefault(maxTries, SubscriptionConstant.DEFAULT_MAX_TRIES)
        self.backOff = ConverterStatic.getValueOrDefault(backOff, SubscriptionConstant.DEFAULT_BACKOFF)
        self.queue = queue


class SubscriptionResponseDto:
    def __init__(self,
        key = None,
        url = None,
        onErrorUrl = None,
        maxTries = None,
        backOff = None,
        queue = None
    ):
        self.key = key
        self.url = url
        self.onErrorUrl = onErrorUrl
        self.maxTries = ConverterStatic.getValueOrDefault(maxTries, SubscriptionConstant.DEFAULT_MAX_TRIES)
        self.backOff = ConverterStatic.getValueOrDefault(backOff, SubscriptionConstant.DEFAULT_BACKOFF)
        self.queue = queue
