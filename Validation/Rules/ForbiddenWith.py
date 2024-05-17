from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class ForbiddenWith(BaseRule):
    name: str = 'forbidden_with'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        relatedParamNames = list(ruleAttributes)

        if data.get(paramName) is not None:
            anyOfRelatedParamsIsPresent = False
            for relatedParamName in relatedParamNames:
                if data.get(relatedParamName) is not None:
                    anyOfRelatedParamsIsPresent = True
                    break
            if anyOfRelatedParamsIsPresent:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.FORBIDDEN_WITH', alteredParamName, ', '.join([f'`{relatedParamName}`' for relatedParamName in relatedParamNames]))
                }))
