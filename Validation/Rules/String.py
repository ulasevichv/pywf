from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Exceptions.Logic.InputParameterException import InputParameterException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class String(BaseTypeRule):
    name: str = 'str'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> str | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)
        except InputParameterException as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex)
            }))

    @classmethod
    def parse(cls, value: Any, paramName: str | None = None) -> str:
        if not isinstance(value, str):
            raise InputParameterException(Lang.msg('VALIDATION.STRING', paramName))

        return value
