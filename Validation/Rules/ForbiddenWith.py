from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class ForbiddenWith(BaseRule):
    name = 'forbidden_with'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        relatedParamNames = list(ruleAttributes)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

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

        return paramValue
