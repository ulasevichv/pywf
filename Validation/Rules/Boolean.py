from typing import Any

from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class Boolean(BaseTypeRule):
    name: str = 'bool'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> bool | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue)
        except ValueError:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.BOOLEAN', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any) -> bool:
        if type(value) is bool:
            return value

        if type(value) is str:
            strValue = str(value).lower()

            if strValue in ['true', '1']:
                return True
            elif strValue in ['false', '0']:
                return False

        if type(value) is int:
            if value == 1:
                return True
            elif value == 0:
                return False

        raise ValueError()
