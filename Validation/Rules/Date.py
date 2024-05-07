from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Date(BaseRule):
    name = 'email'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if not isinstance(paramValue, str):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.STRING', alteredParamName)
            }))

        try:
            return cls.parse(paramValue)[0]
        except ValueError as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex) % alteredParamName
            }))

    @classmethod
    def parse(cls, s: str):
        from datetime import datetime
        import re

        matches = re.findall(MethodsForStrings.getDateRegEx(), s)
        if len(matches) != 0:
            dateStr = matches[0][0]
            startDT = datetime.strptime(dateStr, '%Y-%m-%d')
            endDT = startDT.replace(hour=23, minute=59, second=59)
            return [startDT, endDT]
