from dataclasses import dataclass

from jsonschema import Draft7Validator

from app.functions import MultiValidationError
from app.service.notification.email import EmailAddressee, EmailMessage
from app.util import one_mb_bytes


@dataclass
class SendEmailParams:
    to: str = ''
    to_name: str = ''
    _from: str = ''
    from_name: str = ''
    subject: str = ''
    body: str = ''

    @property
    def sender(self) -> EmailAddressee:
        return EmailAddressee(self.from_name, self._from)

    @property
    def recipient(self) -> EmailAddressee:
        return EmailAddressee(self.to_name, self.to)

    @property
    def message(self) -> EmailMessage:
        return EmailMessage(self.subject, self.body)

    @classmethod
    def validate(cls, json: dict) -> 'SendEmailParams':
        """
        Gets and validates input params from raw input json

        :param json: Deserialized JSON object input

        :return: An instance of this class if input JSON was valid
        :raises: MultiValidationError if input did not pass validation (even if only 1 error occurs, the "multi" class
                                      is raised to make for a simpler interface)
        """

        errors = list(_validator.iter_errors(json))
        if len(errors):
            raise MultiValidationError(errors)

        ctor_params = dict()
        for param_name, param_value in json.items():
            if param_name == 'from':
                param_name = '_from'

            ctor_params[param_name] = param_value

        return cls(**ctor_params)


_is_str_schema = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 300,
}

_is_email_schema = {
    **_is_str_schema,
    'format': 'email',
}

_validator = Draft7Validator({
    'type': 'object',
    'properties': {
        'to': _is_email_schema,
        'to_name': _is_str_schema,
        'from': _is_email_schema,
        'from_name': _is_str_schema,
        'subject': _is_str_schema,
        'body': {**_is_str_schema, 'maxLength': 5 * one_mb_bytes},
    },
    'required': ['to', 'to_name', 'from', 'from_name', 'subject', 'body']
})
