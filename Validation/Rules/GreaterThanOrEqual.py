from ...Exceptions.Http.ValidationException import ValidationException
from ...Helpers.Dict import Dict
from ...Language.Lang import Lang
from .BaseComparisonRule import BaseComparisonRule


class GreaterThanOrEqual(BaseComparisonRule):
    name: str = 'greater_than_or_equal'

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

        if paramParsedValue < relatedParamParsedValue:
            raise ValidationException(Dict({
                alteredParamName: Lang.msg('VALIDATION.COMPARISON.GREATER_THAN_OR_EQUAL', alteredParamName, cls.getAlteredParamName(relatedParamName, paramNamePrefix))
            }))
