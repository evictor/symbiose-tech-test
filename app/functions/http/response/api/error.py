import json
from typing import Optional, Union

from flask import Response
from jsonschema import ValidationError

from app.functions import MultiValidationError
from app.util import json_mime_type


class ApiErrorResponse(Response):
    """A normalized, computer- and human-readable API error response"""

    def __init__(self, status: int, msg: str = '',
                 param_errors: Optional[Union[ValidationError, MultiValidationError]] = None):
        """
        :param status: HTTP status code
        :param msg: Short, human-friendly error message
        :param param_errors: Optional param error(s) details

        Serializes to a JSON response resembling this:

            {
                "status": <int>, # HTTP status code
                "msg": <Optional[str]> # If empty, key will not appear in response

                # If empty, key will not appear in response; a single error passed as ValidationError will be
                # normalized to MultiValidationError of size 1
                "param_errors": <Optional[List[str]]>
            }
        """

        resp_json = {
            'status': status,
        }

        if msg != '':
            resp_json['msg'] = msg

        if param_errors is not None:
            if isinstance(param_errors, ValidationError):
                param_errors = MultiValidationError([param_errors])

            # TODO: This should be List[ParamSet] which would allow for better client machine radability; client could
            #  easily determine which param had error(s) whereas right now parsing of the error message would have to be
            #  implemented
            resp_json['param_errors'] = [e.message for e in param_errors.errors]
            if msg == '':
                resp_json['msg'] = 'See `param_errors` for error details'

        super().__init__(json.dumps(resp_json), status, content_type=json_mime_type)
