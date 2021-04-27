from http.client import UNPROCESSABLE_ENTITY

import flask
from jsonschema import ValidationError
from werkzeug.exceptions import HTTPException

from app.functions import MultiValidationError
from app.functions.http.response.api.error import ApiErrorResponse

app = flask.current_app


@app.errorhandler(Exception)
def base_error_handler(e):
    flask.current_app.logger.warning(e)
    return ApiErrorResponse(500, 'An error occurred on our end and we\'re working on it')


@app.errorhandler(HTTPException)
def http_error_handler(http_error: HTTPException):
    return ApiErrorResponse(http_error.code, http_error.description)


@app.errorhandler(ValidationError)
def validation_error_handler(validation_error: ValidationError):
    return ApiErrorResponse(UNPROCESSABLE_ENTITY, param_errors=validation_error)


@app.errorhandler(MultiValidationError)
def multi_validation_error_handler(errors: MultiValidationError):
    return ApiErrorResponse(UNPROCESSABLE_ENTITY, param_errors=errors)
