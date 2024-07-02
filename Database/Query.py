from re import split as re_split

from ..Database.DB import DB
from ..Database.Expression import Expression
from ..Helpers.Dict import Dict
from ..Helpers.Log import Log
from ..Helpers.MethodsForStrings import MethodsForStrings
from ..Language.Lang import Lang


class Query:
    def __init__(self):
        self._connection = DB.getConnection()
        self._selectFields: list = []
        self._fromClause: str = ''
        self._whereConditions: list = []
        self._whereRawConditions: list = []
        self._orWhereConditions: list = []
        self._ordering: list = []
        self._limitClause: str | None = None
        self._offsetClause: str | None = None

    def _verifyNumberOfFetchedFields(self, exampleRow):
        for fieldName in self._selectFields:
            if fieldName == '*':
                raise Exception(Lang.msg('DB.ASTERIX_USAGE_NOT_SUPPORTED') + '.'
                                + ' ' + 'SQL:' + "\n" + self.buildSql())

        numFieldsExpected = len(self._selectFields)
        numFieldsFetched = len(exampleRow)

        if len(self._selectFields) != len(exampleRow):
            raise Exception(Lang.msg('DB.INVALID_NUMBER_OF_FIELDS_FETCHED', numFieldsExpected, numFieldsFetched) + '.'
                            + ' SQL:' + "\n" + self.buildSql())

    def _prepareOutputFieldNames(self):
        results = []

        for i in range(len(self._selectFields)):
            fieldName = self._selectFields[i]

            # Splitting field name by dot.

            fieldNameParts = fieldName.split('.')
            if len(fieldNameParts) > 2:
                raise Exception(Lang.msg('DB.INVALID_FIELD_NAME') + ': ' + fieldName + '.'
                                + ' ' + 'SQL:' + "\n" + self.buildSql())
            elif len(fieldNameParts) == 2:
                outputFieldName = fieldNameParts[1]
            else:
                outputFieldName = fieldNameParts[0]

            # Splitting field name by "AS".

            fieldNameParts = re_split(' as | AS ', outputFieldName)

            if len(fieldNameParts) > 2:
                raise Exception(Lang.msg('DB.INVALID_FIELD_NAME') + ': ' + outputFieldName + '.'
                                + ' ' + 'SQL:' + "\n" + self.buildSql())
            elif len(fieldNameParts) == 2:
                outputFieldName = fieldNameParts[1]
            else:
                outputFieldName = fieldNameParts[0]

            results.append(outputFieldName)

        return results

    @classmethod
    def _rowToDict(cls, row, outputFieldNames):
        result = Dict()

        for i in range(len(outputFieldNames)):
            outputFieldName = outputFieldNames[i]
            result[outputFieldName] = row[i]

        return result

    @classmethod
    def _escapeFieldName(cls, fieldName: str):
        if not DB.whetherToEscapeFieldNames():
            return fieldName

        parts = fieldName.split('.')
        escapedFieldName = ''
        for i, part in enumerate(parts):
            if i > 0:
                escapedFieldName += '.'
            escapedFieldName += '`' + part + '`'
        return escapedFieldName

    @classmethod
    def _escapeValue(cls, value):
        if (isinstance(value, Expression)
                or str(value).isnumeric()):
            return str(value)
        elif isinstance(value, bool):
            return str(1 if value else 0)
        else:
            return '"' + MethodsForStrings.escapeQuotes(str(value)) + '"'

    def select(self, columns: list | str = None):
        if columns is None:
            columns = ['*']

        if type(columns) is str:
            columns = [columns]

        self._selectFields = columns
        return self

    def from_(self, tableName: str, as_: str = None):
        self._fromClause = self._escapeFieldName(tableName) + ('' if as_ is None else ' AS ' + as_)
        return self

    def fromRaw(self, sql):
        self._fromClause = sql
        return self

    @classmethod
    def _splitOperatorAndValue(cls, operatorOrValue, value=None):
        if value is None:
            operator = '='
            value = operatorOrValue
        else:
            operator = operatorOrValue

        return [operator, value]

    def where(self, fieldName: str, operatorOrValue, value=None):
        operator, value = self._splitOperatorAndValue(operatorOrValue, value)

        self._whereConditions.append(self._escapeFieldName(fieldName) + ' ' + operator + ' ' + self._escapeValue(value))

        return self

    def whereNull(self, fieldName: str):
        self._whereConditions.append(self._escapeFieldName(fieldName) + ' IS NULL')
        return self

    def whereNotNull(self, fieldName: str):
        self._whereConditions.append(self._escapeFieldName(fieldName) + ' IS NOT NULL')
        return self

    def whereRaw(self, value):
        self._whereRawConditions.append(value())

        return self

    def orWhere(self, fieldName: str, operatorOrValue, value=None):
        operator, value = self._splitOperatorAndValue(operatorOrValue, value)

        self._orWhereConditions.append(self._escapeFieldName(fieldName) + ' ' + operator + ' ' + self._escapeValue(value))

        return self

    def orWhereRaw(self, value: str):
        pass

    def order(self, fieldName, direction='ASC'):
        self._ordering.append(fieldName + ' ' + direction)
        return self

    def limit(self, value):
        self._limitClause = value
        return self

    def offset(self, value):
        self._offsetClause = value
        return self

    """ ==================================================
    Build-SQL and data-retrieving methods.
    ================================================== """

    def buildSql(self, addTrailingSemicolon=True):
        sqlFeed = []

        if len(self._selectFields) != 0:
            sqlFeed.append('SELECT ' + ', '.join(self._selectFields))
            sqlFeed.append('FROM ' + self._fromClause)

            if len(self._whereConditions) != 0:
                for i, condition in enumerate(self._whereConditions):
                    if i == 0:
                        sqlFeed.append('WHERE ' + condition)
                    else:
                        sqlFeed.append("\t" + 'AND ' + condition)

            if len(self._whereRawConditions) != 0:
                if len(self._whereConditions) == 0:
                    for i, condition in enumerate(self._whereRawConditions):
                        if i == 0:
                            sqlFeed.append('WHERE ' + condition)
                        else:
                            sqlFeed.append("\t" + 'AND ' + condition)
                else:
                    for i, condition in enumerate(self._whereRawConditions):
                        sqlFeed.append("\t" + 'AND ' + condition)

            if len(self._orWhereConditions) != 0:
                if len(self._whereConditions) == 0:
                    for i, condition in enumerate(self._orWhereConditions):
                        if i == 0:
                            sqlFeed.append('WHERE ' + condition)
                        else:
                            sqlFeed.append("\t" + 'OR ' + condition)
                else:
                    for i, condition in enumerate(self._orWhereConditions):
                        sqlFeed.append("\t" + 'OR ' + condition)

            if len(self._ordering) != 0:
                sqlFeed.append('ORDER BY ' + ', '.join(self._ordering))

            if self._limitClause is not None:
                sqlFeed.append('LIMIT ' + str(self._limitClause))

            if self._offsetClause is not None:
                sqlFeed.append('OFFSET ' + str(self._offsetClause))

        if addTrailingSemicolon:
            sqlFeed[-1] = sqlFeed[-1] + ';'

        rawSql = "\n".join(sqlFeed)

        if DB.whetherToLogSQL:
            Log.info(rawSql)

        return rawSql

    def getOne(self):
        dbCursor = self._connection.cursor()
        dbCursor.execute(self.buildSql())
        rows = dbCursor.fetchall()
        dbCursor.close()

        if len(rows) == 0:
            return None
        elif len(rows) > 1:
            Log.error('Extra rows were fetched from DB on SQL:' + "\n" + self.buildSql())
            row = rows[0]
        else:
            row = rows[0]

        self._verifyNumberOfFetchedFields(row)
        outputFieldNames = self._prepareOutputFieldNames()

        return self._rowToDict(row, outputFieldNames)

    def getAll(self):
        dbCursor = self._connection.cursor()
        dbCursor.execute(self.buildSql())
        rows = dbCursor.fetchall()
        dbCursor.close()

        if len(rows) == 0:
            return []

        self._verifyNumberOfFetchedFields(rows[0])
        outputFieldNames = self._prepareOutputFieldNames()

        results = []
        for row in rows:
            results.append(self._rowToDict(row, outputFieldNames))

        return results

    def getColumn(self, targetFieldName: str | None = None):
        rows = self.getAll()

        if len(rows) == 0:
            return []

        if targetFieldName is None:
            targetFieldName = list(rows[0].keys())[0]

        results = []
        for i, row in enumerate(rows):
            results.append(row[targetFieldName])

        return results

    def getCellValue(self):
        dbCursor = self._connection.cursor()
        dbCursor.execute(self.buildSql())
        rows = dbCursor.fetchall()
        dbCursor.close()

        if len(rows) > 1:
            Log.error('Extra rows were fetched from DB on SQL:' + "\n" + self.buildSql())
            row = rows[0]
        elif len(rows) == 0:
            return None
        else:
            row = rows[0]

        cellValue = row[0]

        return cellValue

    @classmethod
    def _getWhereClauseStr(cls, whereDict: Dict):
        whereClauseFeed = [
            "\t" + 'WHERE',
        ]

        counter = 0
        for key, value in whereDict.items():
            andClause = '    ' if counter == 0 else 'AND '
            counter += 1
            whereClauseFeed.append(andClause + '`' + key + '` = ' + MethodsForStrings.escapeForSQLInsertOrUpdate(value))

        return "\n\t".join(whereClauseFeed)

    def insert(self, tableClass, fieldNames: list[str], valueRows: list[Dict]):
        sqlFeedFirstLine = 'INSERT INTO `' + tableClass.tn() + '` ('
        for i, fieldName in enumerate(fieldNames):
            comma = '' if i == 0 else ', '
            sqlFeedFirstLine += comma + '`' + fieldName + '`'
        sqlFeedFirstLine += ') VALUES'

        sqlFeed = [
            sqlFeedFirstLine
        ]

        for i, valuesRow in enumerate(valueRows):
            comma = '  ' if i == 0 else ', '
            sqlRowStr = "\t" + comma + '('

            sqlRowFeed = []
            for fieldName, value in valuesRow.items():
                sqlRowFeed.append(MethodsForStrings.escapeForSQLInsertOrUpdate(value))

            for j, strValue in enumerate(sqlRowFeed):
                comma = '' if j == 0 else ', '
                sqlRowStr += comma + strValue

            sqlRowStr += ')'

            sqlFeed.append(sqlRowStr)

        sqlFeed[-1] += ';'

        rawSql = "\n".join(sqlFeed)

        if DB.whetherToLogSQL:
            Log.info(rawSql)

        dbCursor = self._connection.cursor()
        dbCursor.execute(rawSql)
        self._connection.commit()
        dbCursor.close()

    def update(self, tableClass, fieldNames: list[str], values: list, whereDict: Dict):
        sqlFeed = [
            'UPDATE `' + tableClass.tn() + '` SET'
        ]

        for i, fieldName in enumerate(fieldNames):
            comma = '  ' if i == 0 else ', '
            sqlRowStr = "\t" + comma + '`' + fieldName + '` = ' + MethodsForStrings.escapeForSQLInsertOrUpdate(values[i])

            sqlFeed.append(sqlRowStr)

        whereClauseStr = type(self)._getWhereClauseStr(whereDict)
        sqlFeed.append(whereClauseStr + ';')

        rawSql = "\n".join(sqlFeed)

        if DB.whetherToLogSQL:
            Log.info(rawSql)

        dbCursor = self._connection.cursor()
        dbCursor.execute(rawSql)
        self._connection.commit()
        dbCursor.close()

    def delete(self, tableClass, whereDict: Dict):
        sqlFeed = [
            'DELETE FROM `' + tableClass.tn() + '`'
        ]

        whereClauseStr = type(self)._getWhereClauseStr(whereDict)
        sqlFeed.append(whereClauseStr + ';')

        rawSql = "\n".join(sqlFeed)

        if DB.whetherToLogSQL:
            Log.info(rawSql)

        dbCursor = self._connection.cursor()
        dbCursor.execute(rawSql)
        self._connection.commit()
        dbCursor.close()

    def executeRawReading(self, rawSql: str):
        if DB.whetherToLogSQL:
            Log.info(rawSql)

        dbCursor = self._connection.cursor()
        dbCursor.execute(rawSql)
        result = dbCursor.fetchall()
        dbCursor.close()

        return result

    def executeRawWriting(self, rawSql: str) -> None:
        if DB.whetherToLogSQL:
            Log.info(rawSql)

        dbCursor = self._connection.cursor()
        dbCursor.execute(rawSql)
        self._connection.commit()
        dbCursor.close()
