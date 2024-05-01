from abc import abstractmethod
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang


class BaseRule:
    name: ''

    @abstractmethod
    def validate(self, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        pass

    @classmethod
    def getAlteredParamName(cls, paramName: str, paramNamePrefix) -> str:
        return paramName if paramNamePrefix == '' else paramNamePrefix + '.' + paramName

    @classmethod
    def getRuleName(cls, rule):
        if isinstance(rule, str):
            return rule.split(':')[0]
        elif isinstance(rule, cls):
            return rule.name
        else:
            raise Exception(Lang.msg('GENERAL.INVALID_TYPE', type(rule).__name__))

    @classmethod
    def isStrByRules(cls, rules):
        from vendor.pywf.Validation.Rules.Email import Email
        from vendor.pywf.Validation.Rules.String import String

        allStrRuleNames = [Email.name, String.name]

        for rule in rules:
            ruleName = cls.getRuleName(rule)

            if ruleName in allStrRuleNames:
                return True

        return False
