from ...Exceptions.Http.ForbiddenException import ForbiddenException
from ...Http.Request import Request
from ...Language.Lang import Lang
from .BaseMiddleware import BaseMiddleware


class CheckJson(BaseMiddleware):
    @classmethod
    def handle(cls, request: Request) -> None:
        requiredContentType = 'application/json'
        requestContentType = request.getContentType()

        if requestContentType is None or requestContentType.lower() != requiredContentType:
            raise ForbiddenException(Lang.msg('AUTH_INVALID_CONTENT_TYPE', requiredContentType))
