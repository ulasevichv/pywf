from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Sometimes(BaseRule):
    name: str = 'sometimes'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        # Logic for this validator is defined inside Validator class.
        return
