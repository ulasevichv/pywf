from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class Array(BaseTypeRule):
    name: str = 'array'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> list | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)
        except (ValueError, TypeError):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.ARRAY', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any, paramName: str | None = None) -> list:
        return list(value)
