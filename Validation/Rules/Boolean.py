from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Boolean(BaseRule):
    name = 'bool'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if type(paramValue) is bool:
            return paramValue

        if type(paramValue) is str:
            strValue = str(paramValue).lower()

            if strValue in ['true', '1']:
                return True
            elif strValue in ['false', '0']:
                return False

        if type(paramValue) is int:
            if paramValue == 1:
                return True
            elif paramValue == 0:
                return False

        raise ValidationException(Dict({
            alteredParamName: Lang.msg('VALIDATION.BOOLEAN', alteredParamName)
        }))
