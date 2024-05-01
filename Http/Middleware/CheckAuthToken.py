from Models.API.Users.User import User
from vendor.pywf.Http.Middleware.BaseMiddleware import BaseMiddleware
from vendor.pywf.Http.Request import Request
from vendor.pywf.Language.Lang import Lang
from vendor.pywf.Validation.Exceptions.Http.ForbiddenException import ForbiddenException


class CheckAuthToken(BaseMiddleware):
    @classmethod
    def handle(cls, request: Request):
        token = request.getHeader('Auth-Token')

        if token is None:
            raise ForbiddenException(Lang.msg('AUTH_TOKEN_MISSING'))

        userId = User.authTokenToUserId(token)

        if userId is None:
            raise ForbiddenException(Lang.msg('AUTH_TOKEN_EXPIRED'))

        User.authorizeUser(userId)
