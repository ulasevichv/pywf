from ...Exceptions.Http.ForbiddenException import ForbiddenException
from ...Http.Request import Request
from ...Language.Lang import Lang
from .BaseMiddleware import BaseMiddleware


class CheckAuthToken(BaseMiddleware):
    @classmethod
    def handle(cls, request: Request) -> None:
        token = request.getHeader('Auth-Token')

        if token is None:
            raise ForbiddenException(Lang.msg('AUTH_TOKEN_MISSING'))

        # App import.
        from Models.API.Users.User import User as APIUser

        userId = APIUser.authTokenToUserId(token)

        if userId is None:
            raise ForbiddenException(Lang.msg('AUTH_TOKEN_EXPIRED'))

        APIUser.authorizeUser(userId)
