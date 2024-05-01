class SearchFilter:
    paramName: str = None
    validationRules: list = None
    dbField: str = None
    dbMatchType: int = None

    def __init__(self, paramName, validationRules, dbField, dbMatchType):
        self.paramName = paramName
        self.validationRules = validationRules
        self.dbField = dbField
        self.dbMatchType = dbMatchType
