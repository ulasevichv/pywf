from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class Integer(BaseTypeRule):
    name: str = 'int'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> int | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)
        except (ValueError, TypeError):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.INTEGER', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any, paramName: str | None = None) -> int:
        if isinstance(value, int):
            return value

        if isinstance(value, (float, complex)):
            raise TypeError

        try:
            return int(value)
        except ValueError:
            raise ValueError
