from ..Helpers.Dict import Dict
from ..Renderers.PlainTextRenderer import PlainTextRenderer
from .BaseRenderer import BaseRenderer


class HtmlRenderer(BaseRenderer):
    contentType: str = 'text/html'

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

        if result.status == '404 Not Found':
            content = '404 - Page Not Found'
        else:
            content = PlainTextRenderer.dictToPlainText(result.errorDict)

        return Dict({
            'status': result.status,
            'headers': [
                ('Content-type', cls.contentType),
            ],
            'body': cls.renderDefaultHTML(content)
        })

    @classmethod
    def renderDefaultHTML(cls, htmlBodyContent: str):
        feed = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            "\t" + '<style>',
            "\t" + 'body {',
            "\t\t" + 'font-family:Monospace,serif;',
            "\t\t" + 'font-size:14px;',
            "\t\t" + 'background-color: #0a141e;',
            "\t\t" + 'color: #969696;',
            "\t\t" + 'cursor:default;',
            "\t" + '}',
            "\t" + '</style>',
            '</head>',
            '</body>',
            htmlBodyContent,
            '</body>',
            '</html>',
        ]

        return "\n".join(feed)
