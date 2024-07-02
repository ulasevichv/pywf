from ..Exceptions.Http.ValidationException import ValidationException
from ..Helpers.Dict import Dict
from ..Http.Request import Request
from ..Validation.Validator import Validator
from ..Language.Lang import Lang

# App import.
from App.Kernel import Kernel


class APIHelper:
    FILTER_MATCH_TYPE_EQUALS = 1
    FILTER_MATCH_TYPE_EQUALS_MULTIPLE = 2
    FILTER_MATCH_TYPE_LIKE = 3
    FILTER_MATCH_TYPE_LIKE_MULTIPLE = 4
    FILTER_MATCH_TYPE_DATE = 5
    FILTER_MATCH_TYPE_DATE_RANGE = 8
    FILTER_RAW = 9
    FILTER_HAVING_RAW = 10

    @classmethod
    def validateAndConvertSearchFilters(cls, request: Request, rootName: str, allowedFilters: list):
        presentFilters = Validator.validateParam(request.body, rootName, {}, ['sometimes', 'object'])  # type: dict

        # Throwing an error on any unrecognized filter.
        allowedFilterNames = []
        for allowedFilter in allowedFilters:
            allowedFilterNames.append(allowedFilter.paramName)
        for presentFilterName in list(presentFilters.keys()):
            if presentFilterName not in allowedFilterNames:
                if Kernel.getApp().envFile.get('APP_DEBUG'):
                    del presentFilters[presentFilterName]
                else:
                    raise ValidationException(Dict({
                        rootName: Lang.msg('VALIDATION.INVALID_FILTER_NAME', rootName + '.' + presentFilterName)
                    }))

        # Validating search filters.
        Validator(presentFilters, cls.getValidationRulesFromAllowedRequestSearchFilters(allowedFilters), rootName).validate()

        # Removing empty filters.
        for presentFilterName in list(presentFilters.keys()):
            value = presentFilters[presentFilterName]
            if value is None or value == '' or (isinstance(value, list) and len(list) == 0):
                del presentFilters[presentFilterName]

        # Converting and returning.
        return cls.convertRequestSearchFiltersIntoDBFilters(presentFilters, allowedFilters)

    @classmethod
    def getValidationRulesFromAllowedRequestSearchFilters(cls, allowedFilters):
        validationRules = Dict()
        for allowedFilter in allowedFilters:
            validationRules[allowedFilter.paramName] = allowedFilter.validationRules
        return validationRules

    @classmethod
    def convertRequestSearchFiltersIntoDBFilters(cls, presentFilters, allowedFilters):
        dbSearchFilters = []
        for presentFilterName in list(presentFilters.keys()):
            value = presentFilters[presentFilterName]
            for allowedFilter in allowedFilters:
                if allowedFilter.paramName != presentFilterName:
                    continue
                dbSearchFilters.append(Dict({
                    'dbField': allowedFilter.dbField,
                    'dbMatchType': allowedFilter.dbMatchType,
                    'value': value,
                }))
        return dbSearchFilters

    @classmethod
    def validateAndConvertSortSettings(cls, request: Request, rootName: str, allowedSortingFields: list) -> list:
        sortSettings = Validator.validateParam(request.body, rootName, [], ['sometimes', 'array'])

        # Validating correct type of each sort setting.

        for i in range(len(sortSettings)):
            sortSetting = sortSettings[i]
            if not isinstance(sortSetting, dict):
                raise ValidationException(Dict({
                    rootName: Lang.msg('SORTING.INVALID_SORT_SETTING_TYPE', rootName, i)
                }))

        # Filtering out any unrecognized sort settings and duplicates.

        allowedShortFieldNames = []
        for item in allowedSortingFields:
            allowedShortFieldNames.append(list(item.keys())[0])

        filteredSortSettings = []
        addedFieldNames = []

        for i, sortSetting in enumerate(sortSettings):
            shortFieldName = list(sortSetting.keys())[0]

            if shortFieldName not in allowedShortFieldNames:
                raise ValidationException(Dict({
                    rootName + '.' + str(i): Lang.msg('SORTING.INVALID_FIELD_NAME', rootName, i)
                }))

            if shortFieldName in addedFieldNames:
                raise ValidationException(Dict({
                    rootName + '.' + str(i): Lang.msg('SORTING.DUPLICATE_FIELD_NAME', rootName, i)
                }))

            filteredSortSettings.append(sortSetting)
            addedFieldNames.append(shortFieldName)

        sortSettings = filteredSortSettings

        # Validating directions and replacing short field names with full ones.

        for i, sortSetting in enumerate(sortSettings):
            shortFieldName = list(sortSetting.keys())[0]
            direction = sortSetting[shortFieldName]

            if not isinstance(direction, str):
                raise ValidationException(Dict({
                    rootName + '.' + str(i): Lang.msg('SORTING.INVALID_DIRECTION_TYPE', rootName, i)
                }))

            if not direction.upper() in ['ASC', 'DESC']:
                raise ValidationException(Dict({
                    rootName + '.' + str(i): Lang.msg('SORTING.INVALID_DIRECTION_VALUE', rootName, i)
                }))

            allowedSortingField = [field for field in allowedSortingFields if list(field.keys())[0] == shortFieldName][0]
            fullFieldName = allowedSortingField[shortFieldName]

            sortSettings[i] = {
                fullFieldName: direction.upper()
            }

        return sortSettings
