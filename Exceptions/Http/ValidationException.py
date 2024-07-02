from .UnprocessableEntityException import UnprocessableEntityException
from ...Helpers.Dict import Dict


class ValidationException(UnprocessableEntityException):
    def __init__(self, *args):
        self.errorBag: Dict | None = None

        if len(args) == 1 and isinstance(args[0], Dict):
            self.errorBag = args[0]
            # Import is here because on top level it leads to an error.
            from ...Language.Lang import Lang
            super().__init__(Lang.msg('VALIDATION.FAILURE'))
            return
        elif len(args) > 1:
            self.errorBag = args[1]

        super().__init__(args[0])

    def addErrorBag(self, bag: Dict):
        self.errorBag = bag

    def __str__(self):
        return super().__str__()
