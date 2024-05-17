from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForMath import MethodsForMath
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Max(BaseRule):
    name: str = 'max'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        maxValue = float(ruleAttributes[0])

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
