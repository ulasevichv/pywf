from abc import abstractmethod

from ...Http.Request import Request


class BaseMiddleware:
    @classmethod
    @abstractmethod
    def handle(cls, request: Request) -> None:
        pass
