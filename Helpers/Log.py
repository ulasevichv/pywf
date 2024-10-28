from datetime import (datetime, timezone)
from os import sep as os_sep


class Log:
    LEVEL_INFO = 0
    LEVEL_WARNING = 1
    LEVEL_ERROR = 2

    @classmethod
    def logEnv(cls, env) -> None:
        feed = ['']
        for k, v in env.items():
            feed.append(f'{k}={v}')
        cls.info("\n".join(feed))
        cls.info(env['wsgi.input'])

    @classmethod
    def levelToStr(cls, level) -> str:
        match level:
            case cls.LEVEL_INFO:
                return 'info'
            case cls.LEVEL_WARNING:
                return 'warning'
            case cls.LEVEL_ERROR:
                return 'error'
            case _:
                from ..Language.Lang import Lang
                raise Exception(Lang.msg('ARGUMENT.INVALID_ENUM_VALUE', level))

    @classmethod
    def log(cls, data, level: int = LEVEL_INFO) -> None:
        if not isinstance(data, str):
            data = str(data)

        logFileName = 'log-' + datetime.now(timezone.utc).strftime('%Y-%m-%d') + '.log'
        logFileRelativePath = os_sep.join(['storage', 'logs', logFileName])
        data = '[' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + '] ' + cls.levelToStr(level).title() + ': ' + data

        from ..Helpers.MethodsForFileSystem import MethodsForFileSystem
        MethodsForFileSystem.writeToFile(logFileRelativePath, data)

    @classmethod
    def info(cls, data) -> None:
        cls.log(data, cls.LEVEL_INFO)

    @classmethod
    def warning(cls, data) -> None:
        cls.log(data, cls.LEVEL_WARNING)

    @classmethod
    def error(cls, data) -> None:
        cls.log(data, cls.LEVEL_ERROR)
