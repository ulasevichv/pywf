from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Nullable(BaseRule):
    name = 'nullable'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        # Logic for this validator is defined inside Validator class.
        return
