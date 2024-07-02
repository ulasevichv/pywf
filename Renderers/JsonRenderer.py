from json import dumps as json_dumps

from ..Helpers.Dict import Dict
from .BaseRenderer import BaseRenderer


class JsonRenderer(BaseRenderer):
    contentType: str = 'application/json'

    @classmethod
    def render(cls, data):
        if data is None:
            data = {}

        return Dict({
            'status': '200 OK',
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': json_dumps(data)
        })

    @classmethod
    def renderException(cls, ex):
        result = super().renderException(ex)

        return Dict({
            'status': result.status,
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': json_dumps(result.errorDict)
        })
