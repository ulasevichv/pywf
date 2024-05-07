from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Http.Request import Request
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ValidationException import ValidationException


class Validator:
    data: list | dict | Request = None
    validationRules: list = None
    errorMessagesPrefix: str = None
    customErrorMessages: list = None

    def __init__(self, data, validationRules, errorMessagesPrefix='', customErrorMessages=None):
        if customErrorMessages is None:
            customErrorMessages = []

        self.data = data
        self.validationRules = validationRules
        self.errorMessagesPrefix = errorMessagesPrefix
        self.customErrorMessages = customErrorMessages

    def validate(self):
        validatedData = Dict({})

        for paramName in self.validationRules:
            allParamRules = self.validationRules[paramName]

            paramPresents = paramName in self.data.getKeys() if type(self.data) is Request else self.data.keys()
            paramValue = self.data.get(paramName)
            alteredParamName = (paramName if self.errorMessagesPrefix == '' else self.errorMessagesPrefix + '.' + paramName)

            try:
                if 'required' in allParamRules and 'sometimes' in allParamRules:
                    raise Exception(Lang.msg('VALIDATION.INVALID_RULES_COMBINATION', 'required', 'sometimes'))

                if 'required' in allParamRules and (paramValue is None or paramValue == '' or paramValue == []):
                    raise ValidationException(Dict({
                        alteredParamName: Lang.msg('VALIDATION.REQUIRED', alteredParamName)
                    }))

                if 'sometimes' in allParamRules and paramValue is None:
                    if paramPresents:
                        validatedData[paramName] = paramValue
                    continue

                if 'nullable' in allParamRules and (paramValue is None or paramValue == '' or paramValue == []):
                    continue

                for rule in allParamRules:
                    if isinstance(rule, str):
                        parts = rule.split(':')

                        ruleName = parts[0]
                        ruleAttributes = [] if len(parts) == 1 else parts[1].split(',')

                        match ruleName:
                            case ('sometimes' | 'required' | 'nullable'):
                                pass

                            # Presence validators.

                            case 'forbidden_with':
                                from vendor.pywf.Validation.Rules.ForbiddenWith import ForbiddenWith
                                paramValue = ForbiddenWith.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)
                            case 'required_without':
                                from vendor.pywf.Validation.Rules.RequiredWithout import RequiredWithout
                                paramValue = RequiredWithout.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)
                            case 'required_mutual_exclude':
                                from vendor.pywf.Validation.Rules.RequiredMutualExclude import RequiredMutualExclude
                                paramValue = RequiredMutualExclude.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)

                            # Type validators.

                            case 'array':
                                from vendor.pywf.Validation.Rules.Array import Array
                                paramValue = Array.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'date':
                                from vendor.pywf.Validation.Rules.Date import Date
                                paramValue = Date.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'dateRange':
                                from vendor.pywf.Validation.Rules.DateRange import DateRange
                                paramValue = DateRange.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'email':
                                from vendor.pywf.Validation.Rules.Email import Email
                                paramValue = Email.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'enum':
                                from vendor.pywf.Validation.Rules.Enum import Enum
                                paramValue = Enum.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)
                            case 'int':
                                from vendor.pywf.Validation.Rules.Integer import Integer
                                paramValue = Integer.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'numeric':
                                from vendor.pywf.Validation.Rules.Numeric import Numeric
                                paramValue = Numeric.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'object':
                                from vendor.pywf.Validation.Rules.Object import Object
                                paramValue = Object.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'phone':
                                from vendor.pywf.Validation.Rules.Phone import Phone
                                paramValue = Phone.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)
                            case 'string':
                                from vendor.pywf.Validation.Rules.String import String
                                paramValue = String.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules)

                            # Limit validators.

                            case 'max':
                                from vendor.pywf.Validation.Rules.Max import Max
                                paramValue = Max.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)
                            case 'min':
                                from vendor.pywf.Validation.Rules.Min import Min
                                paramValue = Min.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)

                            # Unique validators.

                            case 'unique':
                                from vendor.pywf.Validation.Rules.Unique import Unique
                                paramValue = Unique.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)
                            case 'unique_except':
                                from vendor.pywf.Validation.Rules.UniqueExcept import UniqueExcept
                                paramValue = UniqueExcept.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)

                            case _:
                                raise Exception(Lang.msg('VALIDATION.INVALID_RULE_NAME', ruleName))
                    else:
                        raise Exception(Lang.msg('VALIDATION.INVALID_RULE_TYPE_OBJECT'))

                validatedData[paramName] = paramValue

            except ValidationException as ex:
                alteredErrorBag = Dict()
                for key, value in ex.errorBag.items():
                    alteredErrorBag[alteredParamName] = value
                raise ValidationException(alteredErrorBag)

        return validatedData

    @classmethod
    def validateParam(cls, data, paramName, defaultValue, rules):
        paramValue = data.get(paramName, defaultValue)

        cls({
            paramName: paramValue,
        }, {
            paramName: rules,
        }).validate()

        return paramValue

    def getErrors(self) -> Dict:
        try:
            self.validate()
            return Dict()
        except ValidationException as ex:
            return ex.errorBag
