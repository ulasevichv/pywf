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
                return indent + s + indent if indentLength * 2 + strLen == requiredLength else indent + s + indent + patternSymbol
            case 'left':
                return s + indent
            case 'right':
                return indent + s
            case _:
                return s

    """
     * Get string representation of an array of objects (in form of a table).
     *
     * arr                  - Array of objects.
     * displayPropertyNames - Array of property names to display. If empty - all properties will be shown.
     * labels               - Array of labels for header (to replace property names). If empty - property names will be used.
     * alignment            - Alignment (['left', 'right', 'center']).
     * returnAsArray        - Whether to return result as an array of lines.
    """
    @classmethod
    def objectsArrayToStringTable(cls, arr: list[dict], displayPropertyNames: list[str] = None, labels: list[str] = None, alignment: str = 'left', returnAsArray: bool = False
                                  ) -> str | list[str]:
        if displayPropertyNames is None:
            displayPropertyNames = []
        if labels is None:
            labels = []

        feed = []

        numItems = len(arr)

        if numItems == 0:
            feed.append('+=============+')
            feed.append('| Empty table |')
            feed.append('+=============+')
        else:
            if len(displayPropertyNames) == 0:
                for propertyName, value in arr[0].items():
                    displayPropertyNames.append(propertyName)

            numDisplayProperties = len(displayPropertyNames)

            if len(labels) != numDisplayProperties:
                labels = []

            useLabels = (len(labels) != 0)

            # Counting number of symbols in columns.

            numSymbolsByColumns = []

            for k, propertyName in enumerate(displayPropertyNames):
                title = labels[k] if useLabels else propertyName
                columnContentLength = len(title)

                for i in range(0, numItems):
                    cellContent = arr[i][propertyName]

                    if isinstance(cellContent, (dict, list)):
                        cellContentLen = 2
                    else:
                        cellContentLen = len(str(cellContent))

                    # Log.info(str(i) + ' "' + propertyName + '": ' + str(cellValue) + ' -> ' + str(cellContentLen))

                    if cellContentLen > columnContentLength:
                        columnContentLength = cellContentLen

                # Adding 2 additional spaces and storing.
                columnContentLength += 2

                # Log.info(str(k) + ' "' + propertyName + '": ' + str(columnContentLength))

                numSymbolsByColumns.append(columnContentLength)

            # Log.info(numSymbolsByColumns)

            # ==========
            # Creating table head.
            # ==========

            # Line one.

            lineFeed = []

            for k, propertyName in enumerate(displayPropertyNames):
                lineFeed.append('=' * numSymbolsByColumns[k])

            feed.append('+' + '+'.join(lineFeed) + '+')

            # Line two.

            lineFeed = []

            for k, propertyName in enumerate(displayPropertyNames):
                title = labels[k] if useLabels else propertyName
                lineFeed.append(' ' + cls.alignString(title, numSymbolsByColumns[k] - 2, alignment) + ' ')

            feed.append('|' + '|'.join(lineFeed) + '|')

            # Line three.

            feed.append(feed[0])

            # ==========
            # Creating table body.
            # ==========

            for i in range(0, numItems):
                lineFeed = []

                for k, propertyName in enumerate(displayPropertyNames):
                    cellContent = arr[i][propertyName]

                    if isinstance(cellContent, dict):
                        cellContent = '{}'
                    elif isinstance(cellContent, list):
                        cellContent = '[]'
                    else:
                        cellContent = str(cellContent)

                    lineFeed.append(' ' + cls.alignString(cellContent, numSymbolsByColumns[k] - 2, alignment) + ' ')

                feed.append('|' + '|'.join(lineFeed) + '|')

            # ==========
            # Creating table footer.
            # ==========

            lineFeed = []

            for k, propertyName in enumerate(displayPropertyNames):
                lineFeed.append('-' * numSymbolsByColumns[k])

            feed.append('+' + '+'.join(lineFeed) + '+')

        return feed if returnAsArray else "\n".join(feed)
