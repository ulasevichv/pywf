from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Helpers.MethodsForMath import MethodsForMath
from ...Language.Lang import Lang
from .BaseRule import BaseRule


class Min(BaseRule):
    name: str = 'min'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        minValue = float(ruleAttributes[0])

        if isinstance(paramValue, str) and cls.isStrByRules(allParamRules):
            if len(paramValue) < minValue:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.MIN.STR', alteredParamName, minValue)
                }))
        elif MethodsForMath.isNumeric(paramValue):
            paramValue = MethodsForMath.toNumeric(paramValue)
            if paramValue < minValue:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.MIN.NUMERIC', alteredParamName, minValue)
                }))
