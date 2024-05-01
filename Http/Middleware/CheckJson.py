from vendor.pywf.Http.Middleware.BaseMiddleware import BaseMiddleware
from vendor.pywf.Http.Request import Request
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ForbiddenException import ForbiddenException


class CheckJson(BaseMiddleware):
    @classmethod
    def handle(cls, request: Request):
        requiredContentType = 'application/json'
        requestContentType = request.getContentType()

        if requestContentType is None or requestContentType.lower() != requiredContentType:
            raise ForbiddenException(Lang.msg('AUTH_INVALID_CONTENT_TYPE', requiredContentType))
