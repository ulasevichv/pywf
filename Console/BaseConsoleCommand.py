from abc import abstractmethod

from ..Helpers.Dict import Dict
from ..Helpers.Log import Log
from ..Language.Lang import Lang


class BaseConsoleCommand:
    # https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences?redirectedfrom=MSDN#text-formatting

    FORMAT_CODES: Dict = Dict({
        'DEFAULT': 0,
        'BOLD': 1,
        'UNDERLINE': 4,

        'BG_BLACK': 40,
        'BG_RED': 41,
        'BG_GREEN': 42,
        'BG_YELLOW': 43,
        'BG_BLUE': 44,
        'BG_MAGENTA': 45,
        'BG_CYAN': 46,
        'BG_WHITE': 47,

        'BG_BRIGHT_BLACK': 100,
        'BG_BRIGHT_RED': 101,
        'BG_BRIGHT_GREEN': 102,
        'BG_BRIGHT_YELLOW': 103,
        'BG_BRIGHT_BLUE': 104,
        'BG_BRIGHT_MAGENTA': 105,
        'BG_BRIGHT_CYAN': 106,
        'BG_BRIGHT_WHITE': 107,

        'FG_BRIGHT_BLACK': 90,
        'FG_BRIGHT_RED': 91,
        'FG_BRIGHT_GREEN': 92,
        'FG_BRIGHT_YELLOW': 93,
        'FG_BRIGHT_BLUE': 94,
        'FG_BRIGHT_MAGENTA': 95,
        'FG_BRIGHT_CYAN': 96,
        'FG_BRIGHT_WHITE': 97,
    })

    _parsedParams: Dict = None

    @classmethod
    @abstractmethod
    def execute(cls) -> None:
        pass

    @classmethod
    def getApp(cls):
        from App.Kernel import Kernel
        return Kernel.getApp()

    # ==================================================
    # Messages.
    # ==================================================

    @classmethod
    def getFormatByCode(cls, code: int) -> str:
        return '\033[' + str(code) + 'm'

    @classmethod
    def getDefaultFormat(cls) -> str:
        return cls.getFormatByCode(cls.FORMAT_CODES.DEFAULT)

    @classmethod
    def info(cls, data, writeToLog: bool = False) -> None:
        msg = str(data)
        print(msg)
        if writeToLog:
            Log.info(msg)

    @classmethod
    def infoGreen(cls, data, writeToLog: bool = False) -> None:
        msg = f"{cls.getFormatByCode(cls.FORMAT_CODES.FG_BRIGHT_GREEN)}{str(data)}{cls.getDefaultFormat()}"
        print(msg)
        if writeToLog:
            Log.info(msg)

    @classmethod
    def infoBlue(cls, data, writeToLog: bool = False) -> None:
        msg = f"{cls.getFormatByCode(cls.FORMAT_CODES.FG_BRIGHT_BLUE)}{str(data)}{cls.getDefaultFormat()}"
        print(msg)
        if writeToLog:
            Log.info(msg)

    @classmethod
    def warning(cls, data, writeToLog: bool = False) -> None:
        msg = f"{cls.getFormatByCode(cls.FORMAT_CODES.FG_BRIGHT_YELLOW)}{Lang.msg('CONSOLE.WARNING').upper() + ': '}{cls.getDefaultFormat()}" + str(data)
        print(msg)
        if writeToLog:
            Log.info(msg)

    @classmethod
    def error(cls, data, writeToLog: bool = False) -> None:
        msg = f"{cls.getFormatByCode(cls.FORMAT_CODES.FG_BRIGHT_RED)}{Lang.msg('CONSOLE.ERROR').upper() + ': '}{cls.getDefaultFormat()}" + str(data)
        print(msg)
        if writeToLog:
            Log.info(msg)

    # ==================================================
    # Prompts.
    # ==================================================

    @classmethod
    def coloredInput(cls, prompt: str) -> str:
        cls.info('')
        return input(f"{cls.getFormatByCode(cls.FORMAT_CODES.FG_BRIGHT_BLUE)}{prompt + ' (y/n)?'}{cls.getDefaultFormat()}" + "\n")

    @classmethod
    def showUserConfirmationPrompt(cls, prompt: str) -> bool:
        if cls.coloredInput(prompt) != 'y':
            cls.info('... cancelled by user')
            return False
        return True

    # ==================================================
    # Arguments and parameters.
    # ==================================================

    @classmethod
    def getAllArguments(cls) -> list[str]:
        from sys import argv as sys_argv
        return sys_argv[1:]

    @classmethod
    def parseParameters(cls):
        if cls._parsedParams is not None:
            return cls._parsedParams

        allArguments = cls.getAllArguments()
        if len(allArguments) < 2:
            return Dict()

        allParametersExceptCommandName = allArguments[1:]

        cls._parsedParams = Dict()

        for s in allParametersExceptCommandName:
            if s[0:1] != '-':
                raise Exception(Lang.msg('CONSOLE.INVALID_PARAMETER_SYNTAX', s))

            equalitySignIndex = s.find('=')
            if equalitySignIndex == -1:
                raise Exception(Lang.msg('CONSOLE.INVALID_PARAMETER_SYNTAX', s))

            paramName = s[1:equalitySignIndex]

            paramValue = s[equalitySignIndex + 1:]

            cls._parsedParams[paramName] = paramValue

        return cls._parsedParams

    @classmethod
    def getParam(cls, paramName: str, paramType: str = 'str', defaultValue=None):
        parsedParams = cls.parseParameters()

        if paramName not in parsedParams.keys() or parsedParams[paramName] is None or parsedParams[paramName] == '':
            return defaultValue

        paramValue = parsedParams[paramName]

        match paramType:
            case 'str':
                return paramValue
            case 'bool':
                return bool(paramValue)
            case 'int':
                return int(paramValue)
            case _:
                raise Exception(Lang.msg('ARGUMENT.INVALID_ENUM_VALUE', paramType))

    @classmethod
    def getObligatoryParam(cls, paramName: str, paramType: str = 'str'):
        paramValue = cls.getParam(paramName, paramType, None)
        if paramValue is None:
            raise Exception(Lang.msg('CONSOLE.OBLIGATORY_PARAMETER_MISSING', paramName))
        return paramValue
