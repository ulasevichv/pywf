from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseComparisonRule import BaseComparisonRule


class LessThan(BaseComparisonRule):
    name: str = 'less_than'

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

        if paramParsedValue >= relatedParamParsedValue:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.COMPARISON.LESS_THAN', alteredParamName, cls.getAlteredParamName(relatedParamName, paramNamePrefix))
            }))
