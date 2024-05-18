from datetime import datetime, timezone
from typing import Any

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Exceptions.Logic.FormatException import FormatException
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class Date(BaseTypeRule):
    name: str = 'date'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> datetime | None:
        if data.get(paramName) is None:
            return None

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            return cls.parse(paramValue)[0]
        except TypeError:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.STRING', alteredParamName)
            }))
        except FormatException as ex:
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

        if len(matches) == 0:
            raise FormatException(Lang.msg('VALIDATION.DATE.FORMAT', '%s'))

        dateStr = matches[0][0]
        startDT = datetime.strptime(dateStr, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        endDT = startDT.replace(hour=23, minute=59, second=59)
        return [startDT, endDT]
