from python_framework import SchedulerType
from python_framework import Scheduler, SchedulerMethod, WeekDay, WeekDayConstant


@Scheduler(muteLogs=True)
class MessageScheduler:

    @SchedulerMethod(SchedulerType.INTERVAL, seconds=1, instancesUpTo=10)
    def createAllInstantiatedFromMemory(self) :
        self.service.message.createAllInstantiatedFromMemory()


    @SchedulerMethod(SchedulerType.INTERVAL, seconds=0.1, instancesUpTo=100)
    def sendMessageListFromOneQueue(self) :
        self.service.message.sendMessageListFromOneQueue()
