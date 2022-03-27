from python_framework import Enum, EnumItem


@Enum()
class QueueDomainEnumeration :
    API = EnumItem()
    USER = EnumItem()
    ADMIN = EnumItem()


QueueDomain = QueueDomainEnumeration()
