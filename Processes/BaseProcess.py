from App.Kernel import Kernel
from Console.ConsoleApplication import ConsoleApplication


class BaseProcess:
    isExclusive: bool = False
    pidFileRelativePath: str = ''
    redisStartupQueueName: str = ''

    def __init__(self):
        import os

        self.pid: int = os.getpid()
        self.app: ConsoleApplication = ConsoleApplication()
        Kernel.registerApp(self.app)

        self.initialized: bool = self.initialize()
        if not self.initialized:
            # from vendor.pywf.Helpers.Log import Log
            # type(self).logRedisStartupQueue(self.pid)
            return

        # from vendor.pywf.Helpers.Log import Log
        # type(self).logRedisStartupQueue(self.pid)

        self.allStartupParams = type(self).getAllStartupParams()

    def initialize(self) -> bool:
        if not type(self).isExclusive:
            type(self).writeToRedisStartupQueue(self.pid, 0)
            return True

        concurrentProcessPID = type(self).readPIDFromFile()

        if concurrentProcessPID is not None:
            from vendor.pywf.Helpers.Log import Log

            errorMsg = type(self).getConcurrentProcessRunningErrorMessage(self.pid, concurrentProcessPID)

            type(self).writeToRedisStartupQueue(self.pid, errorMsg)
            # Log.warning(errorMsg)

            return False

        type(self).writePIDToFile()
        type(self).writeToRedisStartupQueue(self.pid, 0)

        return True

    @classmethod
    def getAllStartupParams(cls):
        import sys

        return sys.argv[1:]

    @classmethod
    def cleanup(cls):
        cls.cleanPIDFile()

    @classmethod
    def writePIDToFile(cls) -> None:
        if cls.pidFileRelativePath == '':
            return

        import os
        from vendor.pywf.Helpers.MethodsForFileSystem import MethodsForFileSystem
        MethodsForFileSystem.writeToFile(cls.pidFileRelativePath, os.getpid(), 'w')

    @classmethod
    def cleanPIDFile(cls) -> None:
        if not cls.isExclusive or cls.pidFileRelativePath == '':
            return

        from vendor.pywf.Helpers.MethodsForFileSystem import MethodsForFileSystem
        MethodsForFileSystem.writeToFile(cls.pidFileRelativePath, '', 'w')

    @classmethod
    def readPIDFromFile(cls) -> int | None:
        if cls.pidFileRelativePath == '':
            return

        import os
        from vendor.pywf.Helpers.MethodsForFileSystem import MethodsForFileSystem

        if not os.path.exists(MethodsForFileSystem.relativePathToFull(cls.pidFileRelativePath)):
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
        from vendor.pywf.Language.Lang import Lang
        return Lang.msg('PROCESS.LAUNCH_ERROR.ANOTHER_INSTANCE_RUNNING', cls.__name__, str(pid), str(concurrentProcessPID))

    @classmethod
    def getRedisStartupQueueNamePrefix(cls):
        return Kernel.getApp().envFile.get('REDIS_PROJECT_PREFIX') + ':' + cls.redisStartupQueueName + ':'

    @classmethod
    def getRedisStartupQueueName(cls, pid: int):
        return cls.getRedisStartupQueueNamePrefix() + str(pid)

    @classmethod
    def writeToRedisStartupQueue(cls, pid: int, msg: str | int):
        from vendor.pywf.Helpers.Redis import Redis

        Redis.rpush(cls.getRedisStartupQueueName(pid), msg)
        Redis.close()

    @classmethod
    def logRedisStartupQueue(cls, pid: int):
        from vendor.pywf.Helpers.Log import Log
        from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
        from vendor.pywf.Helpers.Redis import Redis

        queueName = cls.getRedisStartupQueueName(pid)
        Log.info('Queue: ' + queueName)
        items = Redis.lrange(queueName, 0, -1)
        Log.info(MethodsForStrings.simpleListToStringTable(items))
        Redis.close()
