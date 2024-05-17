from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Validation.Rules.BaseComparisonRule import BaseComparisonRule


class GreaterThan(BaseComparisonRule):
    name: str = 'greater_than'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        if data.get(paramName) is None:
            return

        alteredParamName = cls.getAlteredParamName(paramName, paramNamePrefix)

        relatedParamName = list(ruleAttributes)[0]

        if data.get(relatedParamName) is None:
            return

        # Parsing and comparing.

        paramParsedValue, relatedParamParsedValue = cls.parseAPairOfComparingParameters(paramName, relatedParamName, data, paramNamePrefix, allParamRules)

        if paramParsedValue <= relatedParamParsedValue:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.COMPARISON.GREATER_THAN', alteredParamName, cls.getAlteredParamName(relatedParamName, paramNamePrefix))
            }))
