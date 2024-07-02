from typing import Self

from ..Database.DB import DB
from ..Exceptions.DB.ModelNotFoundException import ModelNotFoundException
from ..Helpers.Dict import Dict
from ..Helpers.MethodsForDateTime import MethodsForDateTime
from ..Language.Lang import Lang


class BaseDBModel(Dict):
    _tn: str = ''
    _fieldNames: list[str] = []
    _pk: str | list[str] = ''
    _softDeleteFieldName: str | None = None

    def __init__(self, row: Dict | None = None):
        for fieldName in self._fieldNames:
            self.__setattr__(fieldName, None)

        if row is not None:
            for key, value in row.items():
                self.__setattr__(key, value)

        super().__init__()

    def __repr__(self):
        feed = []
        for fieldName in self._fieldNames:
            feed.append(fieldName + ': ' + str(self.__getattr__(fieldName)))

        return '<' + type(self).__name__ + ' DB-record>:' + "\n\t" + "\n\t".join(feed)

    @classmethod
    def tn(cls):
        return cls._tn

    @classmethod
    def pk(cls):
        return cls._pk

    @classmethod
    def getAllFieldNames(cls, prefix=''):
        if prefix == '':
            return cls._fieldNames

        results = []
        for fieldName in cls._fieldNames:
            results.append(prefix + '.' + fieldName)
        return results

    @classmethod
    def find(cls, pkValue: int | str | list[int | str], fieldNames: list[str] = None) -> Self | None:
        fieldNames = fieldNames if fieldNames is not None else cls._fieldNames

        query = (DB.query()
                 .select(fieldNames)
                 .from_(cls.tn())
                 )

        pk = cls._pk

        if type(pk) is list:
            for i, pkFieldName in enumerate(pk):
                query.where(pkFieldName, pkValue[i])
        else:
            pkValue = pkValue if type(pkValue) is list else [pkValue]
            query.where(pk, pkValue[0])

        if cls._softDeleteFieldName is not None:
            query.whereNull(cls._softDeleteFieldName)

        row = query.getOne()

        return None if row is None else cls(row)

    @classmethod
    def findOrFail(cls, pkValue: int | str | list[int | str], fieldNames: list[str] = None) -> Self:
        rec = cls.find(pkValue, fieldNames)

        if rec is None:
            raise ModelNotFoundException(
                Lang.msg('DB.RECORD.NOT_FOUND', cls.__name__,
                         str(pkValue) if type(cls._pk) is str else ', '.join(
                             map(str, pkValue)),
                         '' if cls._softDeleteFieldName is None else ' (can be soft-deleted)'))

        return rec

    def getPkValueAsList(self):
        pk = type(self)._pk

        if type(pk) is list:
            values = []
            for fieldName in pk:
                values.append(self[fieldName])
            return values
        else:
            return [self[pk]]

    def getPkValueAsDict(self):
        pk = type(self)._pk
        pkFieldNames = pk if type(pk) is list else [pk]

        result = Dict()
        for pkFieldName in pkFieldNames:
            result[pkFieldName] = self[pkFieldName]

        return result

    def save(self):
        pk = type(self)._pk

        if type(pk) is not list and self[pk] is None:
            self.insert()
            return

        exists = self.find(self.getPkValueAsList()) is not None

        if exists:
            self.update_()
        else:
            self.insert()

    def insert(self):
        pk = type(self)._pk

        if type(pk) is not list and self[pk] is None:
            newPK = DB.getMaxId(self) + 1
            self[pk] = newPK

        attributesDict = Dict()
        for fieldName in type(self)._fieldNames:
            attributesDict[fieldName] = self.get(fieldName, None)

        DB.query().insert(type(self), type(self)._fieldNames, [
            attributesDict,
        ])

    def update_(self):
        pk = type(self)._pk
        pkFieldNames = pk if type(pk) is list else [pk]

        fieldNamesToUpdate = []
        values = []
        for fieldName in type(self)._fieldNames:
            if fieldName in pkFieldNames:
                continue
            fieldNamesToUpdate.append(fieldName)
            values.append(self.get(fieldName, None))

        DB.query().update(type(self), fieldNamesToUpdate, values, self.getPkValueAsDict())

    def delete(self):
        softDeleteFieldName = type(self)._softDeleteFieldName

        if softDeleteFieldName is None:
            DB.query().delete(type(self), self.getPkValueAsDict())
        else:
            DB.query().update(type(self), [softDeleteFieldName], [MethodsForDateTime.getCurrentTimestampStr()], self.getPkValueAsDict())
