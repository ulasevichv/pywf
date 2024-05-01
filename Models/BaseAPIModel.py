from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Http.Request import Request
from vendor.pywf.Models.BaseDBModel import BaseDBModel
from vendor.pywf.Validation.Exceptions.DB.ModelNotFoundException import ModelNotFoundException
from vendor.pywf.Validation.Exceptions.Http.NotFoundException import NotFoundException
from vendor.pywf.Validation.Validator import Validator


class BaseAPIModel(BaseDBModel):
    MAX_PAGE_SIZE = 300

    @classmethod
    def validateGetRequestId(cls, value, paramName='id'):
        Validator({
            paramName: value
        }, {
            paramName: ['required', 'int', 'min:1']
        }).validate()

        return int(value)

    @classmethod
    def validateGetRequestPaginationParams(cls, pageSize, pageIndex, maxPageSize=MAX_PAGE_SIZE):
        Validator({
            'pageSize': pageSize,
            'pageIndex': pageIndex
        }, {
            'pageSize': ['required', 'int', 'min:1', 'max:' + str(maxPageSize)],
            'pageIndex': ['required', 'int', 'min:0'],
        }).validate()

        return [int(pageSize), int(pageIndex)]

    @classmethod
    def findOrFail404(cls, pkValue):
        try:
            return cls.findOrFail(pkValue)
        except ModelNotFoundException as ex:
            raise NotFoundException(str(ex))

    @classmethod
    def preProcessRequestData(cls, request: Request, preProcessingRules: Dict):
        for paramName, rule in preProcessingRules.items():
            if request.get(paramName) is not None or (request.get(paramName) is None and rule.addIfAbsent):
                request.merge(Dict({
                    paramName: rule.func(request.get(paramName))
                }))
