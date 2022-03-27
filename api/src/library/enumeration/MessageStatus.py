from python_framework import Enum, EnumItem


@Enum()
class MessageStatusEnumeration :
    ACCEPTED = EnumItem()
    SENDING = EnumItem()
    SENT = EnumItem()
    
    ERROR_AT_SENDING = EnumItem()


MessageStatus = MessageStatusEnumeration()
