from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class RequiredMutualExclude(BaseRule):
    name: str = 'required_mutual_exclude'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        from vendor.pywf.Validation.Rules.ForbiddenWith import ForbiddenWith
        from vendor.pywf.Validation.Rules.RequiredWithout import RequiredWithout

        ForbiddenWith.validate(data, paramName, paramNamePrefix, allParamRules, *ruleAttributes)
        RequiredWithout.validate(data, paramName, paramNamePrefix, allParamRules, *ruleAttributes)
