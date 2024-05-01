from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForMath import MethodsForMath
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Min(BaseRule):
    name = 'min'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        minValue = int(ruleAttributes[0])
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if isinstance(paramValue, str) and cls.isStrByRules(allParamRules):
            if len(paramValue) < minValue:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.MIN_STR', alteredParamName, minValue)
                }))
        elif MethodsForMath.isNumeric(paramValue):
            paramValue = MethodsForMath.toNumeric(paramValue)
            if paramValue < minValue:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.MIN_NUMERIC', alteredParamName, minValue)
                }))

        return paramValue
