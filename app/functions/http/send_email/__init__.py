from app.functions.http.response.api.error import ApiErrorResponse
from app.functions.http.send_email.input import SendEmailParams


def send_email(request):
    """
    HTTP POST Google Cloud Function for the send email action. See send_email_samples.http next to this file for
    executable example usages.

    :param flask.Request request:
    :return:
    """

    if request.path != '/email':
        return ApiErrorResponse(404, 'Please POST to /email')
    elif request.method != 'POST':
        return ApiErrorResponse(405, 'HTTP method must be POST')
    elif not request.is_json:
        return ApiErrorResponse(400, 'Request input must be JSON')

    inp = SendEmailParams.validate(request.json)
    # TODO: send email w/ failover

    return 'TODO'
