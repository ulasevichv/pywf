from abc import abstractmethod

from vendor.pywf.Application.BaseWebApplication import BaseWebApplication
from vendor.pywf.Console.BaseConsoleApplication import BaseConsoleApplication


class BaseProcess:
    isExclusive: bool = False
    pidFileRelativePath: str = ''

    @classmethod
    @abstractmethod
    def execute(cls) -> None:
        pass

    # def getRedisQueue

    @classmethod
    def initializeConsoleApp(cls) -> BaseWebApplication | BaseConsoleApplication:
        from App.Kernel import Kernel
        from Console.ConsoleApplication import ConsoleApplication

        app = ConsoleApplication()
        Kernel.registerApp(app)

        return app

    @classmethod
    def writePIDToFile(cls) -> None:
        if cls.pidFileRelativePath == '':
            return

        import os
        from vendor.pywf.Helpers.MethodsForFileSystem import MethodsForFileSystem
        MethodsForFileSystem.writeToFile(cls.pidFileRelativePath, os.getpid(), 'w')

    @classmethod
    def cleanPIDFile(cls) -> None:
        if cls.pidFileRelativePath == '':
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
    def whetherConcurrentProcessIsRunning(cls) -> bool:
        concurrentProcessPID = cls.readPIDFromFile()
        if concurrentProcessPID is None:
            return False

        from vendor.pywf.Helpers.Log import Log
        from vendor.pywf.Language.Lang import Lang
        Log.error(Lang.msg('PROCESS.LAUNCH_ERROR.ANOTHER_INSTANCE_RUNNING', cls.__name__, str(concurrentProcessPID)))
        return True
