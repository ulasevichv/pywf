from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class Required(BaseRule):
    name = 'required'

    @classmethod
    def validate(cls, data, paramName, paramNamePrefix='', allParamRules=None, *ruleAttributes):
        # Logic for this validator is defined inside Validator class.
        return
