from ...Exceptions.Http.ValidationException import ValidationException
from ...Database.DB import DB
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseRule import BaseRule


class UniqueExcept(BaseRule):
    name: str = 'unique_except'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        if data.get(paramName) is None:
            return

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        tableName = str(ruleAttributes[0])
        fieldName = str(ruleAttributes[1])
        exceptFieldName = str(ruleAttributes[2])
        exceptValue = str(ruleAttributes[3])

        query = (DB.query()
                 .select('COUNT(*) AS numRows')
                 .from_(tableName)
                 .where(fieldName, paramValue)
                 .where(exceptFieldName, '!=', exceptValue)
                 )
        rowFound = query.getCellValue() > 0

        if rowFound:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.UNIQUE', alteredParamName.title(), paramValue)
            }))
