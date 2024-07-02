from ..Helpers.Dict import Dict
from .BaseRenderer import BaseRenderer


class PlainTextRenderer(BaseRenderer):
    contentType: str = 'text/plain;charset=utf-8'

    @classmethod
    def render(cls, data):
        return Dict({
            'status': '200 OK',
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': str(data)
        })

    @classmethod
    def renderException(cls, ex):
        result = super().renderException(ex)

        return Dict({
            'status': result.status,
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': cls.dictToPlainText(result.errorDict),
        })

    @classmethod
    def dictToPlainText(cls, d: dict, level=0):
        feed = []
        for key, value in d.items():
            if isinstance(value, (str, int, float, complex)):
                strValue = str(value)
            elif isinstance(value, dict):
                strValue = "\n" + cls.dictToPlainText(value, level + 1)
            elif isinstance(value, list):
                valueFeed = ['[']
                for listItem in value:
                    valueFeed.append(cls.getIndent(level + 1) + listItem)
                valueFeed.append(cls.getIndent(level) + ']')
                strValue = "\n".join(valueFeed)
            else:
                strValue = 'Unserializable value'

            indent = cls.getIndent(level)

            feed.append(indent + key + ': ' + strValue)

        return "\n".join(feed)

    @classmethod
    def getIndent(cls, level: int) -> str:
        indent = ''
        if level > 0:
            for i in range(0, level):
                indent = "\t" + indent
        return indent
