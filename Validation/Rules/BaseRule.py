from abc import abstractmethod
from typing import Any
from typing import Self

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang


class BaseRule:
    name: str = ''

    @classmethod
    @abstractmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> Any | None:
        pass

    @classmethod
    def getAlteredParamName(cls, paramName: str, paramNamePrefix: str = '') -> str:
        return paramName if paramNamePrefix == '' else paramNamePrefix + '.' + paramName

    @classmethod
    def _getRuleName(cls, rule: str | Self) -> str:
        if isinstance(rule, str):
            return rule.split(':')[0]
        elif isinstance(rule, cls):
            return rule.name
        else:
            raise Exception(Lang.msg('ARGUMENT.INVALID_TYPE', type(rule).__name__))

    @classmethod
    def isStrByRules(cls, rules: list[str | Self]) -> bool:
        from vendor.pywf.Validation.Rules.String import String
        from vendor.pywf.Validation.Rules.Email import Email
        from vendor.pywf.Validation.Rules.Phone import Phone

        allStrRuleNames = [String.name, Email.name, Phone.name]

        for rule in rules:
            ruleName = cls._getRuleName(rule)

            if ruleName in allStrRuleNames:
                return True

        return False
