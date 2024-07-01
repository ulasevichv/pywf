from abc import abstractmethod
from typing import Any

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Validation.Rules.BaseRule import BaseRule


class BaseTypeRule(BaseRule):
    name: str = ''

    @classmethod
    @abstractmethod
    def validate(cls, data: Dict, paramName: str, paramNamePrefix: str = '', allParamRules: list = None, *ruleAttributes) -> Any | None:
        pass

    @classmethod
    @abstractmethod
    def parse(cls, value: Any, paramName: str | None = None) -> Any:
        pass
