from ...Helpers.Dict import Dict
from .BaseRule import BaseRule


class RequiredMutualExclude(BaseRule):
    name: str = 'required_mutual_exclude'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        from .ForbiddenWith import ForbiddenWith
        from .RequiredWithout import RequiredWithout

        ForbiddenWith.validate(data, paramName, paramNamePrefix, allParamRules, *ruleAttributes)
        RequiredWithout.validate(data, paramName, paramNamePrefix, allParamRules, *ruleAttributes)
