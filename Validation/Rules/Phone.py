from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Phone(BaseRule):
    name = 'phone'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if not isinstance(paramValue, str):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.STRING', alteredParamName)
            }))

        import re

        if re.match(MethodsForStrings.getPhoneRegEx(), paramValue) is None:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.PHONE', alteredParamName)
            }))

        return paramValue
