from pathlib import Path
import re
import urllib.parse

from vendor.pywf.Exceptions.Http.NotFoundException import NotFoundException
from vendor.pywf.Application.BaseApplication import BaseApplication
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Http.Request import Request


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
        parsedQueryString = urllib.parse.urlparse(queryString)

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
            isApiRoute = (len(queryString) >= 4 and queryString[0:4] == 'api/')

            if isApiRoute:
                from vendor.pywf.Controllers.BaseAPIController import BaseAPIController
                return BaseAPIController.outputException(NotFoundException('Invalid route'))
            else:
                from vendor.pywf.Controllers.BaseWebController import BaseWebController
                return BaseWebController.outputException(NotFoundException())

        from vendor.pywf.Controllers.BaseController import BaseController

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
                + re.sub('{' + cls.getUrlParameterRegExStr() + '}', '(' + cls.getUrlParameterRegExStr() + ')', routeUri)
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

        match = re.match(cls.getRouteRegExStr(routePath), queryPath)

        return match is not None
