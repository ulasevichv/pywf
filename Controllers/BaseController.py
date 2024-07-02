from ..Helpers.Dict import Dict
from ..Helpers.Log import Log
from ..Http.Middleware.BaseMiddleware import BaseMiddleware
from ..Http.Request import Request


class BaseController:
    rendererOverride = None
    _middleware = []

    @classmethod
    def addMiddleware(cls, middlewareClass, exceptMethods=None):
        if exceptMethods is None:
            exceptMethods = []

        cls._middleware.append(Dict({
            'middlewareClass': middlewareClass,
            'exceptMethods': exceptMethods
        }))

    @classmethod
    def execute(cls, method, request: Request, *urlParams):
        # Log.info(cls.__name__ + ': ' + str(len(cls._middleware)))

        for obj in cls._middleware:
            if method in obj.exceptMethods:
                continue
            middlewareClass = obj.middlewareClass  # type: BaseMiddleware
            middlewareClass.handle(request)

        return cls.output(method(request, *urlParams))

    @classmethod
    def output(cls, data, renderer=None):
        if cls.rendererOverride is not None:
            renderer = cls.rendererOverride

        return renderer.render(data)

    @classmethod
    def outputException(cls, ex, renderer):
        if cls.rendererOverride is not None:
            renderer = cls.rendererOverride

        return renderer.renderException(ex)
