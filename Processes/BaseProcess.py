class BaseProcess:
    isExclusive: bool = False
    pidFileRelativePath: str = ''
    redisStartupQueueName: str = ''

    def __init__(self):
        from os import getpid as os_get_pid

        # App import.
        from ....Console.ConsoleApplication import ConsoleApplication

        self.pid: int = os_get_pid()
        self.app: ConsoleApplication = ConsoleApplication()

        # App import.
        from App.Kernel import Kernel

        Kernel.registerApp(self.app)

        self.initialized: bool = self.initialize()
        if not self.initialized:
            # from ..Helpers.Log import Log
            # type(self).logRedisStartupQueue(self.pid)
            return

        # from ..Helpers.Log import Log
        # type(self).logRedisStartupQueue(self.pid)

        self.allStartupParams = type(self).getAllStartupParams()

    def initialize(self) -> bool:
        if not type(self).isExclusive:
            type(self).writeToRedisStartupQueue(self.pid, 0)
            return True

        concurrentProcessPID = type(self).readPIDFromFile()

        if concurrentProcessPID is not None:
            from ..Helpers.Log import Log

            errorMsg = type(self).getConcurrentProcessRunningErrorMessage(self.pid, concurrentProcessPID)

            type(self).writeToRedisStartupQueue(self.pid, errorMsg)
            # Log.warning(errorMsg)

            return False

        type(self).writePIDToFile()
        type(self).writeToRedisStartupQueue(self.pid, 0)

        return True

    @classmethod
    def getAllStartupParams(cls):
        from sys import argv as sys_argv

        return sys_argv[1:]

    @classmethod
    def cleanup(cls):
        cls.cleanPIDFile()

    @classmethod
    def writePIDToFile(cls) -> None:
        if cls.pidFileRelativePath == '':
            return

        from os import getpid as os_get_pid

        from ..Helpers.MethodsForFileSystem import MethodsForFileSystem

        MethodsForFileSystem.writeToFile(cls.pidFileRelativePath, os_get_pid(), 'w')

    @classmethod
    def cleanPIDFile(cls) -> None:
        if not cls.isExclusive or cls.pidFileRelativePath == '':
            return

        from ..Helpers.MethodsForFileSystem import MethodsForFileSystem
        MethodsForFileSystem.writeToFile(cls.pidFileRelativePath, '', 'w')

    @classmethod
    def readPIDFromFile(cls) -> int | None:
        if cls.pidFileRelativePath == '':
            return

        from os.path import exists as os_path_exists

        from ..Helpers.MethodsForFileSystem import MethodsForFileSystem

        if not os_path_exists(MethodsForFileSystem.relativePathToFull(cls.pidFileRelativePath)):
            return

        pidFileLines = MethodsForFileSystem.readFile(cls.pidFileRelativePath)

        if len(pidFileLines) == 0:
            return

        firstLine = pidFileLines[0].strip()

        if firstLine == '':
            return

        try:
            return int(firstLine)
        except ValueError:
            return

    @classmethod
    def getConcurrentProcessRunningErrorMessage(cls, pid: int, concurrentProcessPID: int):
        from ..Language.Lang import Lang
        return Lang.msg('PROCESS.LAUNCH_ERROR.ANOTHER_INSTANCE_RUNNING', cls.__name__, str(pid), str(concurrentProcessPID))

    @classmethod
    def getRedisStartupQueueNamePrefix(cls):
        # App import.
        from App.Kernel import Kernel
        return Kernel.getApp().envFile.get('REDIS_PROJECT_PREFIX') + ':' + cls.redisStartupQueueName + ':'

    @classmethod
    def getRedisStartupQueueName(cls, pid: int):
        return cls.getRedisStartupQueueNamePrefix() + str(pid)

    @classmethod
    def writeToRedisStartupQueue(cls, pid: int, msg: str | int):
        from ..Helpers.Redis import Redis

        Redis.rpush(cls.getRedisStartupQueueName(pid), msg)
        Redis.close()

    @classmethod
    def logRedisStartupQueue(cls, pid: int):
        from ..Helpers.Log import Log
        from ..Helpers.MethodsForStrings import MethodsForStrings
        from ..Helpers.Redis import Redis

        queueName = cls.getRedisStartupQueueName(pid)
        Log.info('Queue: ' + queueName)
        items = Redis.lrange(queueName, 0, -1)
        Log.info(MethodsForStrings.simpleListToStringTable(items))
        Redis.close()

    @classmethod
    def getProcessStartedMessage(cls, messageTemplate: str) -> str:
        from ..Helpers.MethodsForStrings import MethodsForStrings

        return MethodsForStrings.alignString(' [' + messageTemplate + ' started] ', 120, 'center', '=')

    @classmethod
    def logProcessStartedMessage(cls, messageTemplate: str) -> None:
        from ..Helpers.Log import Log

        Log.info(cls.getProcessStartedMessage(messageTemplate))

    @classmethod
    def getProcessFinishedMessage(cls, messageTemplate: str, processStartRelativeTimeSec: float) -> str:
        from time import perf_counter
        from ..Helpers.MethodsForStrings import MethodsForStrings

        durationSec = round(perf_counter() - processStartRelativeTimeSec, 3)

        return MethodsForStrings.alignString(' [' + messageTemplate + ' finished (%s sec)] ' % durationSec, 120, 'center', '=') + "\n"

    @classmethod
    def logProcessFinishedMessage(cls, messageTemplate: str, processStartRelativeTimeSec: float) -> None:
        from ..Helpers.Log import Log

        Log.info(cls.getProcessFinishedMessage(messageTemplate, processStartRelativeTimeSec))
