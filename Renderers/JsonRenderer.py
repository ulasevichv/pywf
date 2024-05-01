import json
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Renderers.BaseRenderer import BaseRenderer


class JsonRenderer(BaseRenderer):
    contentType = 'application/json'

    @classmethod
    def render(cls, data):
        if data is None:
            data = {}

        return Dict({
            'status': '200 OK',
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': json.dumps(data)
        })

    @classmethod
    def renderException(cls, ex):
        result = super().renderException(ex)

        return Dict({
            'status': result.status,
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': json.dumps(result.errorDict)
        })
