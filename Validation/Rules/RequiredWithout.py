from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class RequiredWithout(BaseRule):
    name: str = 'required_without'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        paramValue = data.get(paramName)
        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        relatedParamNames = list(ruleAttributes)

        if paramValue is None:
            allRelatedParamsAreAbsent = True
            for relatedParamName in relatedParamNames:
                if data.get(relatedParamName) is not None:
                    allRelatedParamsAreAbsent = False
                    break
            if allRelatedParamsAreAbsent:
                raise ValidationException(Dict({
                    alteredParamName: Lang.msg('VALIDATION.REQUIRED_WITHOUT', alteredParamName, ', '.join([f'`{relatedParamName}`' for relatedParamName in relatedParamNames]))
                }))
