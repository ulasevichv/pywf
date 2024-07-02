from abc import abstractmethod
from typing import Any

from ...Helpers.Dict import Dict
from ...Helpers.Log import Log
from .BaseRule import BaseRule


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
