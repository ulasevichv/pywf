from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


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
