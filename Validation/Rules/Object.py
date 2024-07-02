from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class Object(BaseTypeRule):
    name: str = 'object'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> Dict | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)
        except TypeError:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.OBJECT', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any, paramName: str | None = None) -> Dict:
        if not isinstance(value, dict):
            raise TypeError

        return Dict(value)
