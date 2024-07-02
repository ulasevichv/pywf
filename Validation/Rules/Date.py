from datetime import (datetime, timezone)
from typing import Any

from ...Exceptions.Http.ValidationException import ValidationException
from ...Exceptions.Logic.InputParameterException import InputParameterException
from ...Helpers.Dict import Dict
from ...Helpers.MethodsForStrings import MethodsForStrings
from ...Language.Lang import Lang
from .BaseTypeRule import BaseTypeRule


class Date(BaseTypeRule):
    name: str = 'date'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> datetime | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue, alteredParamName)[0]
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

        if len(matches) == 0:
            raise InputParameterException(Lang.msg('VALIDATION.DATE.FORMAT', paramName))

        dateStr = matches[0][0]
        startDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        endDT = startDT.replace(hour=23, minute=59, second=59)
        return [startDT, endDT]
