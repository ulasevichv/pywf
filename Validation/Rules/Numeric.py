from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Helpers.MethodsForMath import MethodsForMath
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class Numeric(BaseTypeRule):
    name: str = 'numeric'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> int | float | complex | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)
        except ValueError:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.NUMERIC', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any, paramName: str | None = None) -> int | float | complex:
        return MethodsForMath.toNumeric(value)
