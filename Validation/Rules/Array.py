from typing import Any

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class Array(BaseTypeRule):
    name: str = 'array'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> list | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue)
        except (ValueError, TypeError):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.ARRAY', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any) -> list:
        return list(value)
