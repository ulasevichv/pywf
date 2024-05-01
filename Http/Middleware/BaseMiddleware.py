from abc import abstractmethod
from vendor.pywf.Http.Request import Request


class BaseMiddleware:
    @classmethod
    @abstractmethod
    def handle(cls, request: Request):
        pass
