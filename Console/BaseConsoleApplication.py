from pathlib import Path
import sys

from vendor.pywf.Application.BaseApplication import BaseApplication
from vendor.pywf.Helpers.Log import Log


class BaseConsoleApplication(BaseApplication):
    def __init__(self):
        super().__init__()
        type(self).isConsoleApp = True

    def processRequest(self):
        type(self).rootPath = str(Path('').resolve()).replace("\\", '/')

        Log.info(sys.argv[1:])

        # allRouteFilePaths = self.getAllRouteFilePaths()
        # for filePath in allRouteFilePaths:
        #     with open(filePath) as f:
        #         exec(f.read())

        # print(type(self).rootPath)

    # @classmethod
    # def getAllRouteFilePaths(cls):
    #     filePaths = []
    #     for p in Path(cls.rootPath + '/Routes').rglob('*.py'):
    #         if p.match(Path(__file__).name):
    #             continue
    #         filePath = str(p).replace("\\", '/')
    #         filePaths.append(filePath)
    #     return filePaths
