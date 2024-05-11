from pathlib import Path

from vendor.pywf.Helpers.Dict import Dict


class BaseApplication:
    isConsoleApp: bool = False
    rootPath: str = None
    routeGroups: list = []
    envFile: Dict = None
    languageFilesRelativeDirPath: str = 'Language'
    envFileConversionRules: Dict = Dict({})

    @classmethod
    def getAllRouteFilePaths(cls, relativeRoutesDirPath: str) -> list:
        filePaths = []
        for p in Path(cls.rootPath + '/' + relativeRoutesDirPath).rglob('*.py'):
            if p.match(Path(__file__).name):
                continue
            filePath = str(p).replace("\\", '/')
            filePaths.append(filePath)
        return filePaths

    @classmethod
    def readAllRoutes(cls, relativeRoutesDirPath: str) -> None:
        allRouteFilePaths = cls.getAllRouteFilePaths(relativeRoutesDirPath)
        for filePath in allRouteFilePaths:
            with open(filePath) as f:
                exec(f.read())

        for routeGroup in cls.routeGroups:
            for route in routeGroup['routes']:
                route['uri'] = routeGroup['prefix'] + ('' if routeGroup['prefix'] == '' else '/') + route['uri']

    @classmethod
    def addRouteGroups(cls, routeGroups):
        cls.routeGroups = cls.routeGroups + routeGroups
