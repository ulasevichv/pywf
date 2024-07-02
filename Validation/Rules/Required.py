from ...Helpers.Dict import Dict
from .BaseRule import BaseRule


class Required(BaseRule):
    name: str = 'required'

    @classmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> None:
        # Logic for this validator is defined inside Validator class.
        return
