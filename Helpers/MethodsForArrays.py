from typing import Any

from ..Language.Lang import Lang
from .Dict import Dict
from .Log import Log


class MethodsForArrays:
    @classmethod
    def whetherObjectPropertyMatchesNeedle(cls, objectPropertyValue: Any, needlePropertyValue: Any, comparisonType: str) -> bool:
        # Support of NULL values.
        if needlePropertyValue is None:
            return objectPropertyValue is None

        # Support of not-NULL values.
        if needlePropertyValue == 'NOT_NULL':
            return objectPropertyValue is not None

        match comparisonType:
            case ('regular' | 'strict'):
                return objectPropertyValue == needlePropertyValue
            case 'case_insensitive':
                return str(objectPropertyValue).casefold() == str(needlePropertyValue).casefold()
            case _:
                raise Exception(Lang.msg('ARGUMENT.INVALID_ENUM_VALUE', comparisonType))

    @classmethod
    def findOneInObjectsArray(cls, arr: list, needleProperties: Dict, comparisonTypes: Dict = None) -> Any | None:
        if len(arr) == 0:
            return None

        if comparisonTypes is None:
            comparisonTypes = Dict()

        if len(comparisonTypes) != len(needleProperties):
            for key, needleValue in needleProperties.items():
                if comparisonTypes.get(key) is None:
                    comparisonTypes[key] = 'regular'

        for obj in arr:
            differenceFound = False
            for key, needleValue in needleProperties.items():
                differenceFound = not cls.whetherObjectPropertyMatchesNeedle(obj[key], needleValue, comparisonTypes[key])
                # Log.info(str(obj[key]) + ' [' + type(obj[key]).__name__ + '] <--> ' + str(needleValue) + ' [' + type(needleValue).__name__ + '] (' + comparisonTypes[key] + ')'
                #          + ' => ' + str(differenceFound))
                if differenceFound:
                    break
            if differenceFound:
                continue
            return obj

        return None
