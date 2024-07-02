from ..Exceptions.Http.ValidationException import ValidationException
from ..Helpers.Dict import Dict
from ..Http.Request import Request
from ..Language.Lang import Lang
from .Rules.BaseRule import BaseRule
from .Rules.BaseTypeRule import BaseTypeRule


class Validator:
    data: Dict | Request = None
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

    @classmethod
    def getRuleClassByName(cls, ruleName: str) -> type[BaseRule]:
        match ruleName:
            # General presence rules.

            case 'sometimes':
                from .Rules.Sometimes import Sometimes
                return Sometimes
            case 'required':
                from .Rules.Required import Required
                return Required
            case 'nullable':
                from .Rules.Nullable import Nullable
                return Nullable

            # Presence rules, depending on other parameters.

            case 'forbidden_with':
                from .Rules.ForbiddenWith import ForbiddenWith
                return ForbiddenWith
            case 'required_without':
                from .Rules.RequiredWithout import RequiredWithout
                return RequiredWithout
            case 'required_mutual_exclude':
                from .Rules.RequiredMutualExclude import RequiredMutualExclude
                return RequiredMutualExclude

            # Type rules.

            case 'array':
                from .Rules.Array import Array
                return Array
            case 'bool':
                from .Rules.Boolean import Boolean
                return Boolean
            case 'date':
                from .Rules.Date import Date
                return Date
            case 'dateRange':
                from .Rules.DateRange import DateRange
                return DateRange
            case 'dateTime':
                from .Rules.DateTime import DateTime
                return DateTime
            case 'email':
                from .Rules.Email import Email
                return Email
            case 'int':
                from .Rules.Integer import Integer
                return Integer
            case 'numeric':
                from .Rules.Numeric import Numeric
                return Numeric
            case 'object':
                from .Rules.Object import Object
                return Object
            case 'phone':
                from .Rules.Phone import Phone
                return Phone
            case 'str':
                from .Rules.String import String
                return String

            # Limit rules.

            case 'enum':
                from .Rules.Enum import Enum
                return Enum
            case 'max':
                from .Rules.Max import Max
                return Max
            case 'min':
                from .Rules.Min import Min
                return Min

            # Comparison rules.

            case 'greater_than':
                from .Rules.GreaterThan import GreaterThan
                return GreaterThan
            case 'greater_than_or_equal':
                from .Rules.GreaterThanOrEqual import GreaterThanOrEqual
                return GreaterThanOrEqual
            case 'less_than':
                from .Rules.LessThan import LessThan
                return LessThan
            case 'less_than_or_equal':
                from .Rules.LessThanOrEqual import LessThanOrEqual
                return LessThanOrEqual

            # Unique rules.

            case 'unique':
                from .Rules.Unique import Unique
                return Unique
            case 'unique_except':
                from .Rules.UniqueExcept import UniqueExcept
                return UniqueExcept

            case _:
                raise Exception(Lang.msg('VALIDATION.INVALID_RULE_NAME', ruleName))

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
                    if not isinstance(rule, str):
                        raise Exception(Lang.msg('VALIDATION.INVALID_RULE_TYPE_OBJECT'))

                    parts = rule.split(':')

                    ruleName = parts[0]
                    ruleAttributes = [] if len(parts) == 1 else parts[1].split(',')

                    if ruleName in ['sometimes', 'required', 'nullable']:
                        continue

                    ruleClass = self.getRuleClassByName(ruleName)

                    isTypeRule = issubclass(ruleClass, BaseTypeRule)

                    if isTypeRule:
                        paramValue = ruleClass.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)
                    else:
                        ruleClass.validate(self.data, paramName, self.errorMessagesPrefix, allParamRules, *ruleAttributes)

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
