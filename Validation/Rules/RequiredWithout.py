from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class RequiredWithout(BaseRule):
    name = 'required_without'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        if allParamRules is None:
            allParamRules = []

        paramValue = data.get(paramName)
        relatedParamNames = list(ruleAttributes)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        if data.get(paramName) is None:
            allRelatedParamsAreAbsent = True
            for relatedParamName in relatedParamNames:
                if data.get(relatedParamName) is not None:
                    allRelatedParamsAreAbsent = False
                    break
            if allRelatedParamsAreAbsent:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.REQUIRED_WITHOUT', alteredParamName, ', '.join([f'`{relatedParamName}`' for relatedParamName in relatedParamNames]))
                }))

        return paramValue
