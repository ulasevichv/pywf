from vendor.pywf.Helpers.Dict import Dict


class BaseEN:
    AD: str = 'Access denied'

    @classmethod
    def getConstants(cls) -> Dict:
        return Dict({
            # ==================================================
            # General.
            # ==================================================

            'GENERAL.INVALID_ARGUMENT': 'Invalid argument passed to a function',
            'GENERAL.INVALID_ENUM_VALUE': 'Invalid enumeration value: %s',
            'GENERAL.INVALID_TYPE': 'Invalid type: %s',

            # Authorization.

            'AUTH_INVALID_CONTENT_TYPE': 'Invalid content type. Should be: %s',
            'AUTH_TOKEN_MISSING': 'Authorization token is missing',
            'AUTH_TOKEN_EXPIRED': 'Authorization token has expired',

            # DB.

            'DB.INVALID_FIELD_NAME': 'Invalid field name',
            'DB.ASTERIX_USAGE_NOT_SUPPORTED': '`*` is not supported for SELECT\'s',
            'DB.INVALID_NUMBER_OF_FIELDS_FETCHED': 'Invalid number of fields fetched from DB: %s fields expected, %s fields fetched',
            'DB.RECORD.NOT_FOUND': '%s {%s} is not found%s',
            'DB.COMPOSITE_PK.NOT_SUPPORTED': 'Invalid SQL-expression: composite primary key is not supported. Table name: `%s`',

            # Sorting.

            'SORTING.NOT_AN_ARRAY': 'The `%s` must be an array',
            'SORTING.INVALID_SORT_SETTING_TYPE': 'The `%s.%d` must be an object',
            'SORTING.INVALID_FIELD_NAME': 'The `%s.%d` field name is invalid',
            'SORTING.DUPLICATE_FIELD_NAME': 'The `%s.%d` field name is duplicate',
            'SORTING.INVALID_DIRECTION_TYPE': 'The `%s.%d` direction must be a string',
            'SORTING.INVALID_DIRECTION_VALUE': 'The `%s.%d` direction must be either ASC or DESC',

            # Validation.

            'VALIDATION.INVALID_RULE_NAME': 'Invalid validation rule name: %s',
            'VALIDATION.INVALID_RULE_TYPE_OBJECT': 'Invalid validation rule: object validators are not yet supported',
            'VALIDATION.INVALID_RULES_COMBINATION': 'Invalid rules combination: `%s` and `%s`',
            'VALIDATION.INVALID_FIELD_NAME': 'Invalid field name for validation rule: %s',
            'VALIDATION.INVALID_FILTER_NAME': 'Invalid filter name: %s',
            'VALIDATION.FAILURE': 'Validation failure',
            'VALIDATION.PARAMETER_REQUIRED': 'Parameter `%s` is required',

            'VALIDATION.ARRAY': 'Parameter `%s` must be an array',
            'VALIDATION.DATE': 'Parameter `%s` must be a valid date in format YYYY-MM-DD',
            'VALIDATION.DATE_RANGE.FORMAT': 'Parameter `%s` must be a valid date range in format YYYY-MM-DD / YYYY-MM-DD',
            'VALIDATION.DATE_RANGE.START_GREATER_THAN_END': 'Parameter `%s` is invalid: start date must be less or equal to end date',
            'VALIDATION.EMAIL': 'Parameter `%s` must be a valid email address',
            'VALIDATION.PHONE': 'Parameter `%s` must be a valid phone (7-24 symbols, including only numbers, + and -)',
            'VALIDATION.INTEGER': 'Parameter `%s` must be an integer',
            'VALIDATION.OBJECT': 'Parameter `%s` must be an object',
            'VALIDATION.STRING': 'Parameter `%s` must be a string',

            'VALIDATION.MAX_NUMERIC': 'Parameter `%s` must be <= %d',
            'VALIDATION.MAX_STR': 'Parameter `%s` must not contain more than %d symbols',
            'VALIDATION.MIN_NUMERIC': 'Parameter `%s` must be >= %d',
            'VALIDATION.MIN_STR': 'Parameter `%s` must contain at least %d symbols',
            'VALIDATION.UNIQUE': '%s \'%s\' is already taken',

            # ==================================================
            # Entity-specific.
            # ==================================================

            # User.

            'USER.EMAIL_NOT_FOUND': 'Email not found',
            'USER.WRONG_PASSWORD': 'Wrong password',
            'USER.USER_ROLE_ABSENT': 'User role is absent for user ID=%s',
            'USER.NOT_FOUND': 'User ID=%s is not found',
            'USER.EDIT.ACCESS_DENIED': cls.AD + 'only staff and user himself can edit user details',
            'USER.DELETE.ACCESS_DENIED': cls.AD + 'only staff can delete users',
            'USER.GET_ONE.ACCESS_DENIED': cls.AD + ': ' + 'only staff and user himself can get this information',
            'USER.GET_LIST.ACCESS_DENIED': cls.AD + ': ' + 'only staff can get a list of users',
        })
