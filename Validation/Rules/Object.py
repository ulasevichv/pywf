from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Object(BaseRule):
    name = 'object'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if data.get(paramName) is None:
            return

        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        try:
            if isinstance(paramValue, (str, list)):
                raise ValueError

            return Dict(paramValue)
        except (ValueError, TypeError):
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.OBJECT', alteredParamName)
            }))
