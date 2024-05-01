from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class DateRange(BaseRule):
    name = 'dateRange'

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
            return cls.parse(paramValue)
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

        matches = re.findall(MethodsForStrings.getDateRangeStartOnlyRegEx(), s)
        if len(matches) != 0:
            dateStr = matches[0][0]
            startDT = datetime.strptime(dateStr, '%Y-%m-%d')
            return [startDT, None]

        matches = re.findall(MethodsForStrings.getDateRangeEndOnlyRegEx(), s)
        if len(matches) != 0:
            dateStr = matches[0][0]
            endDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            return [None, endDT]

        matches = re.findall(MethodsForStrings.getDateRangeBothRegEx(), s)
        if len(matches) != 0:
            startDateStr = matches[0][0]
            endDateStr = matches[0][3]
            startDT = datetime.strptime(startDateStr, '%Y-%m-%d')
            endDT = datetime.strptime(endDateStr, '%Y-%m-%d').replace(hour=23, minute=59, second=59)

            if startDT > endDT:
                raise ValueError(Lang.msg('VALIDATION.DATE_RANGE.START_GREATER_THAN_END', '%s'))

            return [startDT, endDT]

        raise ValueError(Lang.msg('VALIDATION.DATE_RANGE.FORMAT', '%s'))
