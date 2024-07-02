from datetime import (datetime, timezone)
from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Exceptions.Logic.InputParameterException import InputParameterException
from ...Helpers.Dict import Dict
from ...Helpers.MethodsForStrings import MethodsForStrings
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class DateRange(BaseTypeRule):
    name: str = 'dateRange'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> list[datetime] | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)
        except (InputParameterException, ValueError) as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex)
            }))

    @classmethod
    def parse(cls, value: Any, paramName: str | None = None) -> list[datetime]:
        if not isinstance(value, str):
            raise InputParameterException(Lang.msg('VALIDATION.STRING', paramName))

        from re import findall as re_findall

        matches = re_findall(MethodsForStrings.getDateRegEx(), value)
        if len(matches) != 0:
            dateStr = matches[0][0]
            startDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            endDT = startDT.replace(hour=23, minute=59, second=59)
            return [startDT, endDT]

        matches = re_findall(MethodsForStrings.getDateRangeStartOnlyRegEx(), value)
        if len(matches) != 0:
            dateStr = matches[0][0]
            startDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            return [startDT, None]

        matches = re_findall(MethodsForStrings.getDateRangeEndOnlyRegEx(), value)
        if len(matches) != 0:
            dateStr = matches[0][0]
            endDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc).replace(hour=23, minute=59, second=59)
            return [None, endDT]

        matches = re_findall(MethodsForStrings.getDateRangeBothRegEx(), value)
        if len(matches) != 0:
            startDateStr = matches[0][0]
            endDateStr = matches[0][3]
            startDT = datetime.strptime(startDateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            endDT = datetime.strptime(endDateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc).replace(hour=23, minute=59, second=59)

            if startDT > endDT:
                raise InputParameterException(Lang.msg('VALIDATION.DATE_RANGE.START_GREATER_THAN_END', paramName))

            return [startDT, endDT]

        raise InputParameterException(Lang.msg('VALIDATION.DATE_RANGE.FORMAT', paramName))
