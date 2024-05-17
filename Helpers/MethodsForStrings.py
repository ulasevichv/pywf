import datetime

from vendor.pywf.Helpers.Log import Log


class MethodsForStrings:
    @classmethod
    def replace(cls, sources: [str], replacements: [str], s: str) -> str:
        from vendor.pywf.Language.Lang import Lang

        if (len(sources) != len(replacements)
                | len(sources) == 0
                | len(replacements) == 0):
            raise Exception(Lang.msg('GENERAL.INVALID_ARGUMENT'))

        for i, source in enumerate(sources):
            replacement = replacements[i]
            s = s.replace(source, replacement)

        return s

    @classmethod
    def escapeQuotes(cls, s: str) -> str:
        return s.replace('"', '\\"')

    @classmethod
    def escapeForSQLInsertOrUpdate(cls, value: str | int | float | complex | datetime.datetime | None):
        from vendor.pywf.Language.Lang import Lang

        if type(value) not in (str, int, float, complex, datetime.datetime) and value is not None:
            raise Exception(Lang.msg('GENERAL.INVALID_TYPE', type(value).__name__))

        if value is None:
            return 'NULL'

        match value:
            case str():
                return '"' + cls.escapeQuotes(value) + '"'
            case int() | float() | complex():
                return str(value)
            case datetime.datetime():
                return '"' + value.strftime('%Y-%m-%d %H:%M:%S') + '"'
            case _:
                raise Exception(Lang.msg('GENERAL.INVALID_TYPE', type(value).__name__))

    @classmethod
    def escapeForSQLLike(cls, s: str) -> str:
        return cls.replace(['%', '_'], ['\\%', '\\_'], s)

    @classmethod
    def strToBool(cls, s: str) -> bool:
        return s == '1' or s.lower() == 'true'

    @classmethod
    def getEmailRegEx(cls):
        return r'^.+@[^.].*\.[a-zA-Z]{2,12}$'

    @classmethod
    def getPhoneRegEx(cls):
        return r'^[+\(0-9]{1,1}[\-\(\)0-9 ]{7,24}$'

    @classmethod
    def getDateRegEx(cls):
        return r'^[ ]*(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))[ ]*$'

    @classmethod
    def getDateRangeStartOnlyRegEx(cls):
        return r'^[ ]*(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))[ ]*\/[ ]*\.\.\.[ ]*$'

    @classmethod
    def getDateRangeEndOnlyRegEx(cls):
        return r'^[ ]*\.\.\.[ ]*\/[ ]*(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))[ ]*$'

    @classmethod
    def getDateRangeBothRegEx(cls):
        return r'^[ ]*(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))[ ]*\/[ ]*(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))[ ]*$'

    @classmethod
    def getDateTimeRegEx(cls):
        return r'^[ ]*(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]))[ ]*$'

    @classmethod
    def generateRandomString(cls, stringLength: int, symbolSet: str = None):
        """
        Generate random string
        :param stringLength: int Required string length.
        :param symbolSet: str | None Set of symbols to use.
        :return: str Generated random string.
        """
        import random

        match symbolSet:
            case 'upper':
                chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            case 'lower':
                chars = '0123456789abcdefghijklmnopqrstuvwxyz'
            case 'letters':
                chars = 'abcdefghijklmnopqrstuvwxyz'
            case 'digits':
                chars = '0123456789'
            case 'all' | _:
                chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        numChars = len(chars)

        feed = []
        for n in range(0, stringLength):
            index = random.randint(0, numChars - 1)
            feed.append(chars[index:index+1])

        return ''.join(feed)

    @classmethod
    def alignString(cls, s: str, requiredLength: int, alignment: str = 'left', patternSymbol: str = ' ') -> str:
        strLen = len(s)

        if strLen == requiredLength:
            return s

        if strLen > requiredLength:
            return s[0:requiredLength]

        import math

        indentLength = math.floor((requiredLength - strLen) / 2) if alignment == 'center' else requiredLength - strLen

        indentFeed = []
        for i in range(0, indentLength):
            indentFeed.append(patternSymbol)
        indent = ''.join(indentFeed)

        match alignment:
            case 'center':
                return indent + s + indent if indentLength * 2 == requiredLength else indent + s + indent + patternSymbol
            case 'left':
                return s + indent
            case 'right':
                return indent + s
            case _:
                return s
