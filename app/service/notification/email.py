import json
from base64 import b64encode
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib.request import Request

from app.config import SENDGRID_API_KEY, MAILGUN_SENDING_API_KEY, MAILGUN_DOMAIN
from app.service.notification import Recipient, Sender, Message
from app.service.notification.webhook import WebhookNotifier
from app.util import json_mime_type, txt_mime_type, form_data_mime_type

"""Chars that need to be stripped from the name and email parts of email HTTP headers to prevent injection"""
_email_header_special_chars = {'\n', '\r', ',', '<', '>'}


def strip_email_header_special_chars(header_value: str) -> str:
    """:return: A version of header_value with chars stripped that can be used for email header injection"""
    return ''.join([ch for ch in header_value if ch not in _email_header_special_chars])


@dataclass
class EmailAddressee(Sender, Recipient):
    name: str

    """Email address"""
    email: str

    @property
    def for_sendgrid_api(self) -> dict:
        """:return: An addressee JSON-like dict for Sendgrid API"""
        return {
            'name': self.name,
            'email': self.email,
        }

    @property
    def for_http_header(self) -> str:
        """:return: The addressee sanitized and formatted for a From or To email HTTP header"""

        name_clean = strip_email_header_special_chars(self.name)
        email_clean = strip_email_header_special_chars(self.email)

        return f'{name_clean} <{email_clean}>'


@dataclass
class EmailMessage(Message):
    subject: str
    body: str

    @property
    def sendgrid_api_fields(self) -> dict:
        """
        :return: A JSON-like dict for Sendgrid API with the message fields. Note that the dict itself is not a
                 standalone entity but rather has its fields merged into the main Sendgrid email object.
        """
        return {
            'subject': self.subject,
            'content': [
                {
                    # TODO: html to plain text
                    'type': txt_mime_type,
                    'value': self.body,
                }
            ]
        }


class SendGridEmailer(WebhookNotifier):
    """See https://sendgrid.com/docs/api-reference/"""

    def __init__(self, api_key: str = SENDGRID_API_KEY):
        self._api_key = api_key
        if not self._api_key:
            raise ValueError('Missing Sendgrid API key settable via env var SENDGRID_API_KEY or constructor param here')

        super().__init__()

    def build_request(self, sender: EmailAddressee, recipient: EmailAddressee, message: EmailMessage) -> Request:
        return Request(
            method='POST',
            url='https://api.sendgrid.com/v3/mail/send',
            data=bytes(json.dumps({
                'from': sender.for_sendgrid_api,
                'personalizations': [
                    {
                        'to': recipient.for_sendgrid_api,
                    }
                ],
                **message.sendgrid_api_fields
            })),
            headers={
                'Authorization': f'Bearer {self._api_key}',
                'Content-Type': json_mime_type,
            }
        )


class MailgunEmailer(WebhookNotifier):
    """See https://documentation.mailgun.com/en/latest/api_reference.html"""

    def __init__(self, api_key: str = MAILGUN_SENDING_API_KEY):
        self._api_key = api_key
        if not self._api_key:
            raise ValueError('Missing Mailgun API key settable via env var MAILGUN_SENDING_API_KEY or constructor param'
                             ' here')

        super().__init__()

    def build_request(self, sender: EmailAddressee, recipient: EmailAddressee, message: EmailMessage) -> Request:
        return Request(
            method='POST',
            url=f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
            data=bytes(urlencode({
                'from': sender.for_http_header,
                'to': recipient.for_http_header,
                'subject': message.subject,
                'text': message.body,
            })),
            headers={
                'Authorization': f'Basic {b64encode("api:" + self._api_key).decode("ascii")}',
                'Content-Type': form_data_mime_type,
            }
        )
