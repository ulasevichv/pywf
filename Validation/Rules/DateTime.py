from datetime import datetime, timezone
from typing import Any

from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Exceptions.Logic.InputParameterException import InputParameterException
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseTypeRule import BaseTypeRule


class DateTime(BaseTypeRule):
    name: str = 'dateTime'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> datetime | None:
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
        except InputParameterException as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex) % alteredParamName
            }))
        except ValueError as ex:
            raise ValidationException(Dict({
                alteredParamName: str(ex)
            }))

    @classmethod
    def parse(cls, value: Any) -> datetime:
        if not isinstance(value, str):
            raise TypeError

        import re

        matches = re.findall(MethodsForStrings.getDateTimeRegEx(), value)

        if len(matches) == 0:
            raise InputParameterException(Lang.msg('VALIDATION.DATE_TIME.FORMAT', '%s'))

        dateStr = matches[0][0]
        dt = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        return dt
