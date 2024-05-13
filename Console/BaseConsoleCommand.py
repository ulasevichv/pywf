from abc import abstractmethod

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang


class BaseConsoleCommand:
    FORMATS: Dict = Dict({
        'COLOR_GREEN': '\033[92m',
        'COLOR_ORANGE': '\033[93m',
        'COLOR_RED': '\033[91m',
        'COLOR_BLUE': '\033[94m',
        'COLOR_CYAN': '\033[96m',
        'COLOR_PINK': '\033[95m',

        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m',
    })

    _parsedParams: Dict = None

    @classmethod
    @abstractmethod
    def execute(cls) -> None:
        pass

    @classmethod
    def info(cls, data) -> None:
        print(str(data))

    @classmethod
    def infoGreen(cls, data) -> None:
        print(f"{cls.FORMATS.COLOR_GREEN}{str(data)}{cls.FORMATS.END}")

    @classmethod
    def warning(cls, data) -> None:
        print(f"{cls.FORMATS.COLOR_ORANGE}{Lang.msg('CONSOLE.WARNING').upper() + ': '}{cls.FORMATS.END}" + str(data))

    @classmethod
    def error(cls, data) -> None:
        print(f"{cls.FORMATS.COLOR_RED}{Lang.msg('CONSOLE.ERROR').upper() + ': '}{cls.FORMATS.END}" + str(data))

    @classmethod
    def getAllArguments(cls) -> list[str]:
        import sys
        return sys.argv[1:]

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
    def getParam(cls, paramName: str, defaultValue=None):
        parsedParamsDict = cls.parseParameters()

        if paramName not in parsedParamsDict.keys():
            return defaultValue

        return parsedParamsDict[paramName]

    @classmethod
    def getObligatoryParam(cls, paramName: str):
        paramValue = cls.getParam(paramName, None)
        if paramValue is None:
            raise Exception(Lang.msg('CONSOLE.OBLIGATORY_PARAMETER_MISSING', paramName))
        return paramValue
