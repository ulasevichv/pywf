from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseRule import BaseRule


class Enum(BaseRule):
    name: str = 'enum'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        if data.get(paramName) is None:
            return

        paramValue = data.get(paramName)
        enumValues = list(ruleAttributes)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if paramValue not in enumValues:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.ENUM', alteredParamName, '[' + ', '.join(enumValues) + ']')
            }))
