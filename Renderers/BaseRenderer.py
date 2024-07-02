from ..Exceptions.Http.ForbiddenException import ForbiddenException
from ..Exceptions.Http.NotFoundException import NotFoundException
from ..Exceptions.Http.UnprocessableEntityException import UnprocessableEntityException
from ..Exceptions.Http.ValidationException import ValidationException
from ..Helpers.Dict import Dict
from ..Helpers.Log import Log


class BaseRenderer:
    contentType: str = None

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
                from traceback import format_exception

                Log.error(''.join(format_exception(ex)))

                status = '500 Internal Server Error'
                errorDict = Dict({
                    'error': 'Something went wrong'
                })

        return Dict({
            'status': status,
            'errorDict': errorDict
        })
