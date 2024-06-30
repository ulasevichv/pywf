import json
from json import JSONDecodeError
import re

from vendor.pywf.Exceptions.Http.ValidationException import ValidationException
from vendor.pywf.Helpers.Dict import Dict


class Request(Dict):
    def __init__(self):
        from App.Kernel import Kernel

        app = Kernel.getApp()

        self.headers = Request.collectHeaders(app.osEnv)
        self.method = Kernel.getApp().osEnv.REQUEST_METHOD
        self.URI = Kernel.getApp().osEnv.REQUEST_URI
        self.urlParams = []
        self.body = Dict()

        super().__init__()

    def __getattr__(self, key):
        try:
            if key in self.keys():
                return self[key]

            if key in self.body.keys():
                return self.body[key]

        except KeyError as ex:
            raise AttributeError(ex)

    def keys(self):
        return super().keys()

    def getKeys(self):
        return self.body.keys()

    def get(self, key: str, default=None):
        keyParts = key.split('.')

        if len(keyParts) == 1:
            if keyParts[0] in self.keys():
                return super().get(keyParts[0], default)
            elif keyParts[0] in self.body.keys():
                return self.body[keyParts[0]]
            return default
        else:
            if keyParts[0] in self.keys():
                nestedObj = super().get(keyParts[0], None)
            elif keyParts[0] in self.body.keys():
                nestedObj = self.body[keyParts[0]]
            else:
                return default

            if isinstance(nestedObj, dict):
                remainingKey = '.'.join(keyParts[1:])
                return self._unpack(nestedObj, remainingKey, default)
            else:
                return default

    @classmethod
    def _unpack(cls, obj: dict, key: str, default=None):
        keyParts = key.split('.')

        if len(keyParts) == 1:
            if keyParts[0] in obj.keys():
                return obj.get(keyParts[0], default)
            return default
        else:
            if keyParts[0] in obj.keys():
                nestedObj = obj.get(keyParts[0], None)
                if isinstance(nestedObj, dict):
                    remainingKey = '.'.join(keyParts[1:])
                    return cls._unpack(nestedObj, remainingKey, default)
                else:
                    return default
            return default

    @classmethod
    def collectHeaders(cls, env: Dict):
        validHeaders = {
            'CONTENT_TYPE': 'Content-Type',
            'HTTP_AUTH_TOKEN': 'Auth-Token',
            'HTTP_USER_AGENT': 'User-Agent',
            'HTTP_ACCEPT': 'Accept',
            'HTTP_POSTMAN_TOKEN': 'Postman-Token',
            'HTTP_HOST': 'Host',
            'HTTP_ACCEPT_ENCODING': 'Accept-Encoding',
            'HTTP_CONNECTION': 'Connection',
        }

        results = Dict()

        for key in validHeaders:
            if key in env.keys():
                value = env[key]
                results[validHeaders[key]] = value

        return results

    def getHeader(self, name: str):
        if name not in self.headers.keys():
            return None
        return self.headers[name]

    def collectUrlParams(self, matchingRoutePath, queryPath):
        from App.Kernel import Kernel
        app = Kernel.getApp()

        expectedParameterNames = re.findall('{' + app.getUrlParameterRegExStr() + '}', matchingRoutePath)

        if len(expectedParameterNames) == 0:
            self.urlParams = []
            return

        values = re.findall(app.getRouteRegExStr(matchingRoutePath), queryPath)
        if len(values) == 0:
            self.urlParams = []
            return

        values = values[0]

        if type(values) is tuple:
            self.urlParams = list(values)
            return

        self.urlParams = [values]

    def getContentType(self):
        return self.headers['Content-Type'] if 'Content-Type' in self.headers.keys() else None

    def processBody(self):
        from App.Kernel import Kernel
        app = Kernel.getApp()

        rawBody = app.osEnv['wsgi.input'].read()

        if len(rawBody) != 0:
            try:
                bodyStr = str(rawBody, 'utf-8')
                decodedBody = json.loads(bodyStr)
                # Log.info(decodedBody)
                # Log.info(decodedBody.__class__.__name__)
                self.body = Dict(decodedBody)

            except JSONDecodeError as ex:
                raise ValidationException('Invalid JSON format of request body')
            except BaseException as ex:
                raise ValidationException('Invalid request body')

    def only(self, paramNames: list[str]):
        results = Dict()

        for key in paramNames:
            if key in self.body.keys():
                results[key] = self.body[key]

        return results

    def merge(self, data: Dict):
        self.body = self.body | data
