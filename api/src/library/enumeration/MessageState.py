from python_framework import Enum, EnumItem


@Enum()
class MessageStateEnumeration :
    INSTANTIATED = EnumItem()
    PERSISTED = EnumItem()
    PROCESSED = EnumItem()


MessageState = MessageStateEnumeration()
