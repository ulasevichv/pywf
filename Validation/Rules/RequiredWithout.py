from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseRule import BaseRule


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
