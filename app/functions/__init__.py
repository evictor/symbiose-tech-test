import dataclasses
from dataclasses import dataclass
from json import JSONEncoder
from typing import Iterable, Set

from jsonschema import ValidationError


@dataclass
class ParamErrorSet(JSONEncoder):
    """
    A non-empty set of errors for a given param

    TODO: Introduce List[ParamSet] in place of List[str] simple error messages in ApiErrorResponse.param_errors
    """

    param_name: str
    errors: Set[ValidationError]

    def __post_init__(self):
        self.errors = set(self.errors)

        if len(self.errors) == 0:
            raise ValueError(f'Expected at least 1 error for ParamErrorSet {self}')

    class JsonEncoder(JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o) and isinstance(o, ParamErrorSet):
                return {
                    'param_name': repr(o),
                    'errors': [e.message for e in o.errors]
                }
            else:
                return super().default(o)


class MultiValidationError(Exception):
    """A consolidated, raiseable error that acts as a non-empty list of jsonschema ValidationErrors"""

    def __init__(self, validation_errors: Iterable[ValidationError]):
        self.errors = list(validation_errors)
        if len(self.errors) == 0:
            raise ValueError('MultiValidationError must represent at least 1 error')
