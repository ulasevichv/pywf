from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Rules.BaseRule import BaseRule
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class RequiredMutualExclude(BaseRule):
    name = 'required_mutual_exclude'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        from vendor.pywf.Validation.Rules.ForbiddenWith import ForbiddenWith
        from vendor.pywf.Validation.Rules.RequiredWithout import RequiredWithout

        ForbiddenWith.validate(data, paramName, paramNamePrefix, allParamRules, *ruleAttributes)
        RequiredWithout.validate(data, paramName, paramNamePrefix, allParamRules, *ruleAttributes)

        return data.get(paramName)
