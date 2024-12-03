from pathlib import Path
from re import (sub as re_sub,
                match as re_match)
from urllib import parse as urllib_parse

from ..Exceptions.Http.NotFoundException import NotFoundException
from ..Application.BaseApplication import BaseApplication
from ..Helpers.Log import Log
from ..Helpers.Dict import Dict
from ..Http.Request import Request


class BaseWebApplication(BaseApplication):
    headersFlushed: bool = False
    osEnv: Dict = None
    request: Request = None

    def __init__(self, env: dict):
        super().__init__()
        type(self).isConsoleApp = False
        type(self).osEnv = Dict(env)
        type(self).rootPath = str(Path(self.osEnv.DOCUMENT_ROOT + '/..').resolve()).replace("\\", '/')

    def processRequest(self):
        type(self).request = Request()

        requestMethod = self.request.method
        queryString = self.request.URI
        if queryString[0] == '/':
            queryString = queryString[1:]
        parsedQueryString = urllib_parse.urlparse(queryString)

        self.readAllRoutes('Routes')

        matchingRoute = None
        for routeGroup in self.routeGroups:
            for route in routeGroup['routes']:
                if self.whetherRouteMatchesQuery(route, requestMethod, parsedQueryString.path):
                    matchingRoute = route
                    break
            if matchingRoute is not None:
                break

        if matchingRoute is None:
            from ..Controllers.BaseWebController import BaseWebController
            return BaseWebController.outputException(NotFoundException())

        from ..Controllers.BaseController import BaseController

        controllerClass = matchingRoute['method'].__self__  # type: BaseController

        try:
            self.request.collectUrlParams(matchingRoute['uri'], parsedQueryString.path)
            self.request.processBody()

            return controllerClass.execute(matchingRoute['method'], self.request, *self.request.urlParams)
        except BaseException as ex:
            return controllerClass.outputException(ex)

    @classmethod
    def getUrlParameterRegExStr(cls) -> str:
        return '[a-zA-Z0-9_\\-\\.@]+'

    @classmethod
    def getRouteRegExStr(cls, routeUri: str) -> str:
        return ('^'
                + re_sub('{' + cls.getUrlParameterRegExStr() + '}', '(' + cls.getUrlParameterRegExStr() + ')', routeUri)
                + '$')

    @classmethod
    def stripTrailingSlash(cls, text: str) -> str:
        if len(text) > 0 and text[-1] == '/':
            return text[:-1]
        return text

    @classmethod
    def whetherRouteMatchesQuery(cls, route: dict, requestMethod: str, parsedQueryString: str) -> bool:
        if requestMethod != route['type']:
            return False

        routePath = cls.stripTrailingSlash(route['uri'])
        queryPath = cls.stripTrailingSlash(parsedQueryString)

        match = re_match(cls.getRouteRegExStr(routePath), queryPath)

        return match is not None
