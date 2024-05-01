# from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Self
import urllib.parse

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForFileSystem import MethodsForFileSystem
from vendor.pywf.Http.Request import Request
from vendor.pywf.Validation.Exceptions.Http.NotFoundException import NotFoundException


class BaseWebApplication:
    app: Self | None = None
    routeGroups = []
    headersFlushed: bool = False

    env: Dict = None
    localEnv: Dict = None
    rootPath: str = None
    rootPath2: str = None
    request: Request = None

    def __init__(self):
        if type(self).app is not None:
            raise Exception('Only one instance of application is allowed')
        type(self).app = self
        BaseWebApplication.app = self

    def processRequest(self, env: dict, startResponse):
        type(self).env = Dict(env)
        type(self).rootPath = str(Path(self.env.DOCUMENT_ROOT + '/..').resolve()).replace("\\", '/')
        type(self).rootPath2 = str(Path('/..').resolve()).replace("\\", '/')
        type(self).localEnv = MethodsForFileSystem.readEnvFile(self.rootPath + '/' + '.env', self.getEnvFileConversionRules())
        type(self).request = Request()

        # Log.logEnv(self.env)
        # Log.info(self.app)
        # Log.info(BaseWebApplication.app)

        requestMethod = self.request.method
        queryString = self.request.URI
        if queryString[0] == '/':
            queryString = queryString[1:]
        parsedQueryString = urllib.parse.urlparse(queryString)

        allRouteFilePaths = self.getAllRouteFilePaths()
        for filePath in allRouteFilePaths:
            with open(filePath) as f:
                exec(f.read())

        for routeGroup in self.routeGroups:
            for route in routeGroup['routes']:
                route['uri'] = routeGroup['prefix'] + ('' if routeGroup['prefix'] == '' else '/') + route['uri']

        matchingRoute = None
        for routeGroup in self.routeGroups:
            for route in routeGroup['routes']:
                if self.whetherRouteMatchQuery(route, requestMethod, parsedQueryString):
                    matchingRoute = route
                    break
            if matchingRoute is not None:
                break

        # # return self.debug('aaa')
        # # return self.debug(123123)
        # # return self.debug(['aaa', 'bbb', 'ccc'])
        # # return self.debug(('aaa', 'bbb', 'ccc'))

        # return self.debug(Dict({
        #     'queryString': queryString,
        #     'matchingRoute': matchingRoute,
        #     'allRouteFilePaths': allRouteFilePaths,
        #     # 'routes': self.routeGroups,
        # }))

        # Log.info(matchingRoute)

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
    def getAllRouteFilePaths(cls):
        filePaths = []
        for p in Path(cls.rootPath + '/Routes').rglob('*.py'):
            if p.match(Path(__file__).name):
                continue
            filePath = str(p).replace("\\", '/')
            filePaths.append(filePath)
        return filePaths

    @classmethod
    def addRouteGroups(cls, routeGroups):
        cls.routeGroups = cls.routeGroups + routeGroups

    @classmethod
    def getUrlParameterRegExStr(cls):
        return '[a-zA-Z0-9_\\-\\.@]+'

    @classmethod
    def getRouteRegExStr(cls, routeUri):
        return ('^'
                + re.sub('{' + cls.getUrlParameterRegExStr() + '}', '(' + cls.getUrlParameterRegExStr() + ')', routeUri)
                + '$')

    @classmethod
    def stripTrailingSlash(cls, text):
        if len(text) > 0 and text[-1] == '/':
            return text[:-1]
        return text

    @classmethod
    def whetherRouteMatchQuery(cls, route, requestMethod, parsedQueryString):
        if requestMethod != route['type']:
            return False

        routePath = cls.stripTrailingSlash(route['uri'])
        queryPath = cls.stripTrailingSlash(parsedQueryString.path)

        # from vendor.pywf.Helpers.Log import Log
        # Log.info('==> ' + queryPath + ' <== checking ==> ' + routePath + ' <***> ' + cls.getRouteRegExStr(routePath))

        match = re.match(cls.getRouteRegExStr(routePath), queryPath)

        return match is not None

    # ==================================================
    # Environment.
    # ==================================================

    @classmethod
    def getLanguageFilesDirName(cls):
        return 'Language'

    @classmethod
    def getEnvFileConversionRules(cls):
        return Dict({
            'APP_DEBUG': 'bool',
            'APP_DEBUG_LOG_SQL': 'bool'
        })

    # ==================================================
    # Debugging.
    # ==================================================

    @classmethod
    def debug(cls, data):
        res = Dict()
        if isinstance(data, str):
            res.value = data
        elif isinstance(data, (int, float, complex)):
            res.value = str(data)
        elif isinstance(data, list):
            res.data = []
            for item in data:
                res.data.append(str(item))
        elif isinstance(data, tuple):
            res.data = []
            for item in data:
                res.data.append(str(item))
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    res[key] = value
                elif isinstance(value, dict):
                    res[key] = Dict()
                    for key2, value2 in value.items():
                        res[key][key2] = str(value2)
                else:
                    res[key] = str(value)
        else:
            res.value = str(data)

        return Dict({
            'status': '200 OK',
            'headers': [
                # ('Content-type', 'text/plain'),
                ('Content-type', 'application/json'),
            ],
            # 'body': "\n".join(feed)
            'body': json.dumps(res)
        })
