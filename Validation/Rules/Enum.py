from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class Enum(BaseRule):
    name = 'enum'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        enumValues = list(ruleAttributes)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if paramValue not in enumValues:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.ENUM', alteredParamName, '[' + ', '.join(enumValues) + ']')
            }))

        return paramValue
