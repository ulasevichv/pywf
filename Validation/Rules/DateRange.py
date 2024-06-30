from datetime import datetime, timezone
from typing import Any

from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Exceptions.Logic.InputFormatException import InputFormatException
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class DateRange(BaseTypeRule):
    name: str = 'dateRange'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> list[datetime] | None:
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
        except InputFormatException as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex) % alteredParamName
            }))
        except ValueError as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex)
            }))

    @classmethod
    def parse(cls, value: Any) -> list[datetime]:
        if not isinstance(value, str):
            raise TypeError

        import re

        matches = re.findall(MethodsForStrings.getDateRegEx(), value)
        if len(matches) != 0:
            dateStr = matches[0][0]
            startDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            endDT = startDT.replace(hour=23, minute=59, second=59)
            return [startDT, endDT]

        matches = re.findall(MethodsForStrings.getDateRangeStartOnlyRegEx(), value)
        if len(matches) != 0:
            dateStr = matches[0][0]
            startDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            return [startDT, None]

        matches = re.findall(MethodsForStrings.getDateRangeEndOnlyRegEx(), value)
        if len(matches) != 0:
            dateStr = matches[0][0]
            endDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc).replace(hour=23, minute=59, second=59)
            return [None, endDT]

        matches = re.findall(MethodsForStrings.getDateRangeBothRegEx(), value)
        if len(matches) != 0:
            startDateStr = matches[0][0]
            endDateStr = matches[0][3]
            startDT = datetime.strptime(startDateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            endDT = datetime.strptime(endDateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc).replace(hour=23, minute=59, second=59)

            if startDT > endDT:
                raise InputFormatException(Lang.msg('VALIDATION.DATE_RANGE.START_GREATER_THAN_END', '%s'))

            return [startDT, endDT]

        raise InputFormatException(Lang.msg('VALIDATION.DATE_RANGE.FORMAT', '%s'))
