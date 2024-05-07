from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForMath import MethodsForMath
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class Numeric(BaseRule):
    name = 'numeric'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if not MethodsForMath.isNumeric(paramValue):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.NUMERIC', alteredParamName)
            }))

        return paramValue
