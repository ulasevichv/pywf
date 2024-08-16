from typing import Any

from .Log import Log


class MethodsForMath:
    @classmethod
    def isNumeric(cls, value: Any) -> bool:
        try:
            cls.toNumeric(value)
            return True
        except ValueError:
            return False

    @classmethod
    def toNumeric(cls, value: Any) -> int | float | complex:
        if isinstance(value, (int, float, complex)):
            return value

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        try:
            return complex(value)
        except ValueError:
            pass

        from ..Language.Lang import Lang
        raise ValueError(Lang.msg('ARGUMENT.NOT_NUMERIC'))

    @classmethod
    def splitIntervalIntoGroups(cls, startIndex: int, endIndex: int, groupSize: int) -> list[list[int]]:
        if endIndex < startIndex or groupSize < 1:
            from inspect import currentframe
            from ..Language.Lang import Lang
            raise ValueError(Lang.msg('ARGUMENT.INVALID_ARGUMENT', cls.__name__ + '.' + currentframe().f_code.co_name + '()'))

        length = endIndex - startIndex + 1

        if groupSize >= length:
            return [[startIndex, endIndex]]

        numGroups = length // groupSize
        remainder = length % groupSize

        if remainder != 0:
            numGroups += 1

        results = []
        for i in range(numGroups):
            groupStartIndex = startIndex + groupSize * i
            groupEndIndex = groupStartIndex + groupSize - 1
            if groupEndIndex > endIndex:
                groupEndIndex = endIndex

            results.append([groupStartIndex, groupEndIndex])

        return results
