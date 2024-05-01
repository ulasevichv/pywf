from os import sep
from pathlib import Path
from datetime import datetime


class Log:
    LEVEL_INFO = 0
    LEVEL_WARNING = 1
    LEVEL_ERROR = 2

    @classmethod
    def writeToFile(cls, fileRelativePath, value):
        if not isinstance(value, str):
            value = str(value)

        from App.App import App
        rootAppPath = Path(App.rootPath)
        # from vendor.pywf.Application.BaseWebApplication import BaseWebApplication
        # rootAppPath = Path(BaseWebApplication.app.rootPath)
        filePath = rootAppPath.joinpath(fileRelativePath)

        Path(sep.join(str(filePath).split(sep)[:-1])).mkdir(parents=True, exist_ok=True)

        f = open(filePath, 'a')
        f.write(value + "\n\n")
        f.close()

    @classmethod
    def logEnv(cls, env):
        feed = ['']
        for k, v in env.items():
            feed.append(f'{k}={v}')
        cls.info("\n".join(feed))
        cls.info(env['wsgi.input'])

    @classmethod
    def levelToStr(cls, level):
        match level:
            case cls.LEVEL_INFO:
                return 'info'
            case cls.LEVEL_WARNING:
                return 'warning'
            case cls.LEVEL_ERROR:
                return 'error'
            case _:
                from vendor.pywf.Language.Lang import Lang
                raise Exception(Lang.msg('GENERAL.INVALID_ENUM_VALUE', level))

    @classmethod
    def log(cls, value, level=LEVEL_INFO):
        if not isinstance(value, str):
            value = str(value)

        logFileName = 'log-' + datetime.utcnow().strftime('%Y-%m-%d') + '.log'
        logFileRelativePath = sep.join(['storage', 'logs', logFileName])
        value = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' [' + cls.levelToStr(level).upper() + ']: ' + value

        cls.writeToFile(logFileRelativePath, value)

    @classmethod
    def info(cls, value):
        cls.log(value, cls.LEVEL_INFO)

    @classmethod
    def warning(cls, value):
        cls.log(value, cls.LEVEL_WARNING)

    @classmethod
    def error(cls, value):
        cls.log(value, cls.LEVEL_ERROR)
