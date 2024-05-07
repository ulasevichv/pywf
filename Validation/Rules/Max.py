from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForMath import MethodsForMath
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class Max(BaseRule):
    name = 'max'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        maxValue = float(ruleAttributes[0])
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if isinstance(paramValue, str) and cls.isStrByRules(allParamRules):
            if len(paramValue) > maxValue:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.MAX.STR', alteredParamName, maxValue)
                }))
        elif MethodsForMath.isNumeric(paramValue):
            paramValue = MethodsForMath.toNumeric(paramValue)
            if paramValue > maxValue:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.MAX.NUMERIC', alteredParamName, maxValue)
                }))

        return paramValue
