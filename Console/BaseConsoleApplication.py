from pathlib import Path

from vendor.pywf.Application.BaseApplication import BaseApplication
from vendor.pywf.Console.BaseConsoleCommand import BaseConsoleCommand
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Language.Lang import Lang


class BaseConsoleApplication(BaseApplication):
    def __init__(self):
        super().__init__()
        type(self).isConsoleApp = True
        type(self).rootPath = str(Path('').resolve()).replace("\\", '/')

    def processRequest(self):
        self.readAllRoutes('Console/Routes')

        allArguments = BaseConsoleCommand.getAllArguments()

        if len(allArguments) == 0:
            BaseConsoleCommand.error(Lang.msg('CONSOLE.NO_COMMAND'))
            return

        commandName = allArguments[0]

        matchingRoute = None
        for routeGroup in self.routeGroups:
            for route in routeGroup['routes']:
                if self.whetherRouteMatchesQuery(route['uri'], commandName):
                    matchingRoute = route
                    break
            if matchingRoute is not None:
                break

        if matchingRoute is None:
            BaseConsoleCommand.error(Lang.msg('CONSOLE.INVALID_COMMAND_NAME', commandName))

        matchingRoute['method']()

    @classmethod
    def whetherRouteMatchesQuery(cls, routeUri: str, commandName: str) -> bool:
        return routeUri.lower() == commandName.lower()
