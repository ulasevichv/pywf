from typing import Any

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForMath import MethodsForMath
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class Numeric(BaseTypeRule):
    name: str = 'numeric'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> int | float | complex | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue)
        except ValueError:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.NUMERIC', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any) -> int | float | complex:
        return MethodsForMath.toNumeric(value)
