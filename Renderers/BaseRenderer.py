import traceback

from vendor.pywf.Exceptions.Http.ForbiddenException import ForbiddenException
from vendor.pywf.Exceptions.Http.NotFoundException import NotFoundException
from vendor.pywf.Exceptions.Http.UnprocessableEntityException import UnprocessableEntityException
from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log


class BaseRenderer:
    contentType = None

    @classmethod
    def render(cls, data):
        pass

    @classmethod
    def renderException(cls, ex):
        match ex.__class__.__name__:
            case NotFoundException.__name__:
                status = '404 Not Found'
                errorDict = Dict({
                    'error': str(ex)
                })
            case ForbiddenException.__name__:
                status = '403 Forbidden'
                errorDict = Dict({
                    'error': str(ex)
                })
            case UnprocessableEntityException.__name__:
                status = '422 Unprocessable Content'
                errorDict = Dict({
                    'error': str(ex)
                })
            case ValidationException.__name__:
                status = '422 Unprocessable Content'
                errorDict = Dict({
                    'error': str(ex),
                    'validationErrors': ex.errorBag
                })
            case _:
                Log.error(''.join(traceback.format_exception(ex)))

                status = '500 Internal Server Error'
                errorDict = Dict({
                    'error': 'Something went wrong'
                })

        return Dict({
            'status': status,
            'errorDict': errorDict
        })
