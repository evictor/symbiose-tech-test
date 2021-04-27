import json

from flask import Response

from app.util import json_mime_type


class ApiErrorResponse(Response):
    """A normalized, computer- and human-readable API error response"""

    def __init__(self, status: int, msg: str = ''):
        """
        :param status: HTTP status code
        :param msg: Short, human-friendly error message

        Serializes to a JSON response resembling this:

            {
                "status": <int>, # HTTP status code
                "msg": <Optional[str]> # If empty, key will not appear in response
            }
        """

        resp_json = {
            'status': status,
        }

        if msg != '':
            resp_json['msg'] = msg

        super().__init__(json.dumps(resp_json), status, content_type=json_mime_type)
