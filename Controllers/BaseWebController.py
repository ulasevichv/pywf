from vendor.pywf.Controllers.BaseController import BaseController
from vendor.pywf.Renderers.HtmlRenderer import HtmlRenderer


class BaseWebController(BaseController):
    @classmethod
    def output(cls, data, renderer=HtmlRenderer):
        return super().output(data, renderer)

    @classmethod
    def outputException(cls, ex, renderer=HtmlRenderer):
        return super().outputException(ex, renderer)
