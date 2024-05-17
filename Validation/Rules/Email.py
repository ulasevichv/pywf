from typing import Any

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Exceptions.Logic.FormatException import FormatException
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class Email(BaseTypeRule):
    name: str = 'email'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> str | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue)
        except TypeError:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.STRING', alteredParamName)
            }))
        except FormatException:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.EMAIL', alteredParamName)
            }))

    @classmethod
    def parse(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError

        import re

        if re.match(MethodsForStrings.getEmailRegEx(), value) is None:
            raise FormatException

        return value
