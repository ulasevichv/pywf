from ..Helpers.Dict import Dict
from ..Helpers.Log import Log


class Lang:
    _currentLanguage: str = None
    _languageClass = None
    _languageConstants: Dict = None

    @classmethod
    def getCurrentLanguageName(cls):
        if cls._currentLanguage is None:
            # App import.
            from App.Kernel import Kernel
            cls._currentLanguage = Kernel.getApp().envFile.get('LANG').upper()
        return cls._currentLanguage

    @classmethod
    def getLanguageClass(cls):
        if cls._languageClass is None:
            langName = cls.getCurrentLanguageName()

            from importlib import import_module
            from inspect import (getmembers as inspect_getmembers, isclass as inspect_isclass)
            from sys import modules as sys_modules

            # App import.
            from App.Kernel import Kernel

            try:
                res = import_module(Kernel.getApp().languageFilesRelativeDirPath + '.' + langName)
            except ModuleNotFoundError as ex:
                raise Exception('Language file is absent: ' + str(ex))

            clsMembers = inspect_getmembers(sys_modules[res.__name__], inspect_isclass)
            for clsInfo in clsMembers:
                if clsInfo[0] != langName:
                    continue
                cls._languageClass = clsInfo[1]

            if cls._languageClass is None:
                raise Exception('Invalid class name inside language file: ' + Kernel.getApp().languageFilesRelativeDirPath + '.' + langName)

        return cls._languageClass

    @classmethod
    def loadConstants(cls):
        if cls._languageConstants is None:
            cls._languageConstants = cls.getLanguageClass().getConstants()

    @classmethod
    def msg(cls, constantName, *values):
        cls.loadConstants()
        return cls._languageConstants[constantName] % values
