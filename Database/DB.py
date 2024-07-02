from ..Helpers.APIHelper import APIHelper
from ..Helpers.Dict import Dict
from ..Helpers.Log import Log
from ..Helpers.MethodsForStrings import MethodsForStrings
from ..Language.Lang import Lang

# App import.
from App.Kernel import Kernel


class DB:
    _connection = None
    whetherToLogSQL: bool = False

    @classmethod
    def getConnection(cls):
        import mysql.connector

        if cls._connection is None:
            app = Kernel.getApp()

            cls.whetherToLogSQL = app.envFile.get('APP_DEBUG_LOG_SQL')

            cls._connection = mysql.connector.connect(
                host=app.envFile.get('DB_HOST'),
                user=app.envFile.get('DB_USERNAME'),
                password=app.envFile.get('DB_PASSWORD'),
                database=app.envFile.get('DB_DATABASE'),
            )

        return cls._connection

    @classmethod
    def query(cls):
        from ..Database.Query import Query
        return Query()

    @classmethod
    def whetherToEscapeFieldNames(cls):
        return not Kernel.getApp().envFile.get('APP_DEBUG')

    @classmethod
    def raw(cls, value):
        from ..Database.Expression import Expression
        return Expression(value)

    @classmethod
    def applySearchFiltersToQuery(cls, query, searchFilters: list[Dict]):
        # Log.info(searchFilters)

        # searchFilters = searchFilters + [
        #     Dict({
        #         'dbField': 'u.name',
        #         'dbMatchType': APIHelper.FILTER_MATCH_TYPE_RAW,
        #         'value': 'LIKE %admin%',
        #     })
        # ]

        for fil in searchFilters:
            match fil.dbMatchType:
                case APIHelper.FILTER_MATCH_TYPE_EQUALS:
                    query.where(fil.dbField, fil.value)

                case APIHelper.FILTER_MATCH_TYPE_LIKE:
                    query.where(fil.dbField, 'LIKE', '%' + MethodsForStrings.escapeForSQLLike(fil.value) + '%')

                case (APIHelper.FILTER_MATCH_TYPE_EQUALS_MULTIPLE
                        | APIHelper.FILTER_MATCH_TYPE_LIKE_MULTIPLE):
                    if isinstance(fil.value, list):
                        values = fil.value
                    else:
                        values = fil.value.split('|')

                    for i, value in enumerate(values):
                        values[i] = value.strip()

                    for value in values:
                        if fil.dbMatchType == APIHelper.FILTER_MATCH_TYPE_EQUALS_MULTIPLE:
                            query.orWhere(fil.dbField, value)
                        else:
                            query.orWhere(fil.dbField, 'LIKE', '%' + MethodsForStrings.escapeForSQLLike(value) + '%')

                case APIHelper.FILTER_MATCH_TYPE_DATE:
                    from ..Validation.Rules.Date import Date

                    startDT = endDT = None
                    try:
                        startDT, endDT = Date.parse(fil.value)
                    except ValueError:
                        pass

                    if startDT is not None:
                        query.where(fil.dbField, '>=', startDT.strftime('%Y-%m-%d %H:%M:%S'))
                    if endDT is not None:
                        query.where(fil.dbField, '<=', endDT.strftime('%Y-%m-%d %H:%M:%S'))

                case APIHelper.FILTER_MATCH_TYPE_DATE_RANGE:
                    from ..Validation.Rules.DateRange import DateRange

                    startDT = endDT = None
                    try:
                        startDT, endDT = DateRange.parse(fil.value)
                    except ValueError:
                        pass

                    if startDT is not None:
                        query.where(fil.dbField, '>=', startDT.strftime('%Y-%m-%d %H:%M:%S'))
                    if endDT is not None:
                        query.where(fil.dbField, '<=', endDT.strftime('%Y-%m-%d %H:%M:%S'))

                case APIHelper.FILTER_RAW:
                    query.whereRaw(fil.dbField)

                case APIHelper.FILTER_HAVING_RAW:
                    pass

                case _:
                    raise Exception(Lang.msg('ARGUMENT.INVALID_ENUM_VALUE', fil.dbMatchType))

    @classmethod
    def applySortSettingsToQuery(cls, query, sortSettings, defaultSortSettings=None):
        if defaultSortSettings is None:
            defaultSortSettings = []

        if len(sortSettings) == 0:
            sortSettings = defaultSortSettings

        for sortSetting in sortSettings:
            fullFieldName = list(sortSetting.keys())[0]
            direction = sortSetting[fullFieldName]
            query.order(fullFieldName, direction)

    @classmethod
    def applyPaginationToQuery(cls, query, pageSize, pageIndex):
        if pageSize is None or pageIndex is None:
            return

        query.limit(int(pageSize)).offset(int(pageSize) * int(pageIndex))

    @classmethod
    def countAllRowsForQuery(cls, query, countingFieldName='id'):
        query = (DB.query()
                 .select(['COUNT(sourceQuery.' + countingFieldName + ') AS counter'])
                 .fromRaw('(' + query.buildSql(False) + ') AS sourceQuery')
                 )

        return int(query.getCellValue())

    @classmethod
    def getMaxId(cls, tableClass) -> int:
        if type(tableClass.pk()) is not str:
            raise Exception(Lang.msg('DB.COMPOSITE_PK.NOT_SUPPORTED', tableClass.tn()))

        return int(cls.query().executeRawReading('SELECT MAX(`' + tableClass.pk() + '`) FROM `' + tableClass.tn() + '`;')[0][0])
