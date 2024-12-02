from ..Controllers.BaseController import BaseController
from ..Helpers.Log import Log
from ..Http.Request import Request
from ..Renderers.JsonRenderer import JsonRenderer
from ..Renderers.HtmlRenderer import HtmlRenderer


class BaseAPIController(BaseController):
    @classmethod
    def output(cls, data, renderer=JsonRenderer):
        return super().output(data, renderer)

    @classmethod
    def outputException(cls, ex, renderer=JsonRenderer):
        return super().outputException(ex, renderer)

    @classmethod
    def renderAPILogo(cls, request: Request):
        cls.rendererOverride = HtmlRenderer

        feed = [
            "\t" + '<pre>',
            '  ______   _______   ______        _______                         __     ',
            ' /      \ /       \ /      |      /       \                       /  |    ',
            '/$$$$$$  |$$$$$$$  |$$$$$$/       $$$$$$$  |  ______    ______   _$$ |_   ',
            '$$ |__$$ |$$ |__$$ |  $$ |        $$ |__$$ | /      \  /      \ / $$   |  ',
            '$$    $$ |$$    $$/   $$ |        $$    $$&lt; /$$$$$$  |/$$$$$$  |$$$$$$/',
            '$$$$$$$$ |$$$$$$$/    $$ |        $$$$$$$  |$$ |  $$ |$$ |  $$ |  $$ | __ ',
            '$$ |  $$ |$$ |       _$$ |_       $$ |  $$ |$$ \__$$ |$$ \__$$ |  $$ |/  |',
            '$$ |  $$ |$$ |      / $$   |      $$ |  $$ |$$    $$/ $$    $$/   $$  $$/ ',
            '$$/   $$/ $$/       $$$$$$/       $$/   $$/  $$$$$$/   $$$$$$/     Z$$$/  ',
            "\t" + '</pre>',
        ]

        return HtmlRenderer.renderDefaultHTML("\n".join(feed))
