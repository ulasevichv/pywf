from ..Helpers.Dict import Dict


class BaseEN:
    AD: str = 'Access denied'

    @classmethod
    def getConstants(cls) -> Dict:
        return Dict({

            # Arguments.

            'ARGUMENT.INVALID_ARGUMENT': 'Invalid argument passed to a function %s',
            'ARGUMENT.INVALID_ENUM_VALUE': 'Invalid enumeration value: %s',
            'ARGUMENT.INVALID_TYPE': 'Invalid type: %s',
            'ARGUMENT.NOT_NUMERIC': 'Value cannot be converted to any numeric type',

            # Authorization.

            'AUTH_INVALID_CONTENT_TYPE': 'Invalid content type. Should be: %s',
            'AUTH_TOKEN_MISSING': 'Authorization token is missing',
            'AUTH_TOKEN_EXPIRED': 'Authorization token has expired',

            # Console.

            'CONSOLE.ERROR': 'Error',
            'CONSOLE.WARNING': 'Warning',
            'CONSOLE.NO_COMMAND': 'No command specified. Use `py cli.py test/test` syntax',
            'CONSOLE.INVALID_COMMAND_NAME': 'Specified command name is not recognized: `%s`',
            'CONSOLE.INVALID_PARAMETER_SYNTAX': 'Invalid parameter syntax: `%s`',
            'CONSOLE.OBLIGATORY_PARAMETER_MISSING': 'Obligatory parameter `%s` is missing',

            # DB.

            'DB.INVALID_FIELD_NAME': 'Invalid field name',
            'DB.ASTERIX_USAGE_NOT_SUPPORTED': '`*` is not supported for SELECT\'s',
            'DB.INVALID_NUMBER_OF_FIELDS_FETCHED': 'Invalid number of fields fetched from DB: %s fields expected, %s fields fetched',
            'DB.RECORD.NOT_FOUND': '%s {%s} is not found%s',
            'DB.COMPOSITE_PK.NOT_SUPPORTED': 'Invalid SQL-expression: composite primary key is not supported. Table name: `%s`',

            # External services.

            'EXTERNAL_SERVICE.INVALID_RESPONSE_STATUS_CODE': 'External service returned invalid status code: %s',
            'EXTERNAL_SERVICE.INVALID_RESPONSE_CONTENT_TYPE': 'External service returned invalid content type: %s',

            # Processes.

            'PROCESS.LAUNCH_ERROR.TIMEOUT': 'Error on process launch: process didn\'t respond in time',
            'PROCESS.LAUNCH_ERROR.ANOTHER_INSTANCE_RUNNING': 'Error on `%s` %s process launch: concurrent process %s is still running',

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

            'VALIDATION.FORBIDDEN_WITH': 'Parameter `%s` is forbidden when any of the following parameters is present: %s',
            'VALIDATION.REQUIRED': 'Parameter `%s` is required',
            'VALIDATION.REQUIRED_WITHOUT': 'Parameter `%s` is required when none of the following parameters is present: %s',

            'VALIDATION.ARRAY': 'Parameter `%s` must be an array',
            'VALIDATION.BOOLEAN': 'Parameter `%s` must be boolean',
            'VALIDATION.DATE.FORMAT': 'Parameter `%s` must be a valid date value in format YYYY-MM-DD',
            'VALIDATION.DATE_RANGE.FORMAT': 'Parameter `%s` must be a valid date-range value in format YYYY-MM-DD / YYYY-MM-DD',
            'VALIDATION.DATE_RANGE.START_GREATER_THAN_END': 'Parameter `%s` is invalid: start date must be less or equal to end date',
            'VALIDATION.DATE_TIME.FORMAT': 'Parameter `%s` must be a valid date-time value in format YYYY-MM-DD HH:mm:SS',
            'VALIDATION.EMAIL': 'Parameter `%s` must be a valid email address',
            'VALIDATION.ENUM': 'Parameter `%s` must belong to enumeration %s',
            'VALIDATION.INTEGER': 'Parameter `%s` must be an integer',
            'VALIDATION.NUMERIC': 'Parameter `%s` must be numeric',
            'VALIDATION.OBJECT': 'Parameter `%s` must be an object',
            'VALIDATION.PHONE': 'Parameter `%s` must be a valid phone (7-24 symbols, including only numbers, + and -)',
            'VALIDATION.STRING': 'Parameter `%s` must be a string',

            'VALIDATION.MAX.NUMERIC': 'Parameter `%s` must be <= %f',
            'VALIDATION.MAX.STR': 'Parameter `%s` must not contain more than %d symbols',
            'VALIDATION.MIN.NUMERIC': 'Parameter `%s` must be >= %f',
            'VALIDATION.MIN.STR': 'Parameter `%s` must contain at least %d symbols',

            'VALIDATION.COMPARISON.MISSING_COMPARABLE_TYPE': 'Validation rule `%s` requires parameter `%s` to be of a comparable type: %s',
            'VALIDATION.COMPARISON.GREATER_THAN': 'Parameter `%s` must be greater than parameter `%s`',
            'VALIDATION.COMPARISON.GREATER_THAN_OR_EQUAL': 'Parameter `%s` must be greater than or equal to parameter `%s`',
            'VALIDATION.COMPARISON.LESS_THAN': 'Parameter `%s` must be less than parameter `%s`',
            'VALIDATION.COMPARISON.LESS_THAN_OR_EQUAL': 'Parameter `%s` must be less than or equal to parameter `%s`',

            'VALIDATION.UNIQUE': '%s \'%s\' is already taken',
        })
