from abc import abstractmethod

from ...Helpers.Dict import Dict
from ...Helpers.Log import Log
from ...Language.Lang import Lang
from .BaseRule import BaseRule


class BaseComparisonRule(BaseRule):
    name: str = ''

    comparableTypeRuleNames: list[str] = ['int', 'numeric', 'date', 'dateTime']

    @classmethod
    @abstractmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        pass

    @classmethod
    def _detectComparableTypeRuleName(cls, paramName: str, allParamRules: list = None) -> str:
        if allParamRules is None:
            allParamRules = []

        for typeRuleName in cls.comparableTypeRuleNames:
            if typeRuleName in allParamRules:
                return typeRuleName

        raise Exception(Lang.msg('VALIDATION.COMPARISON.MISSING_COMPARABLE_TYPE', cls.__name__, paramName, '[' + ', '.join(cls.comparableTypeRuleNames) + ']'))

    @classmethod
    def parseAPairOfComparingParameters(cls, firstParamName: str, secondParamName: str, data: Dict, paramNamePrefix: str = '', allParamRules: list = None):
        # Both comparing parameters must be of the same type.
        bothParamsTypeRuleName = cls._detectComparableTypeRuleName(firstParamName, allParamRules)

        from .BaseTypeRule import BaseTypeRule
        from ...Validation.Validator import Validator

        bothParamsTypeRuleClass = Validator.getRuleClassByName(bothParamsTypeRuleName)  # type: type[BaseTypeRule]

        firstParamParsedValue = bothParamsTypeRuleClass.validate(data, firstParamName, paramNamePrefix)
        secondParamParsedValue = bothParamsTypeRuleClass.validate(data, secondParamName, paramNamePrefix)

        return firstParamParsedValue, secondParamParsedValue
