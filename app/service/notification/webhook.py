from abc import ABC
from urllib.request import Request

from app.service.notification import Notifier, Recipient, Sender, Message, NotifyResult


class WebhookNotifier(Notifier, ABC):
    """Sends notifications via webhook"""

    def build_request(self, sender: Sender, recipient: Recipient, message: Message) -> Request:
        raise NotImplementedError('Subclasses must implement this to create the Webhook Request')

    def notify(self, sender: Sender, recipient: Recipient, message: Message) -> NotifyResult:
        # TODO
        raise NotImplementedError('TODO: implement me')