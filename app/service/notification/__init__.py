from abc import ABC
from dataclasses import dataclass


@dataclass
class NotifyResult:
    """Result of a notification"""
    success: bool

    """
    The number of different Notifier services that were attempted in producing this result; the lowest this can be in
    practice is 1, as in the case that the first notifier attempted succeeds. The highest this can be as in the case of
    NotifierWithFailover is the number of notifiers in the list _n_, as in the case when _n_ - 1 notifiers fail and the
    _n_th notifier must be attempted.
    """
    num_notifiers_attempted: int = 0


@dataclass
class Sender(ABC):
    """Sender of a notification"""


@dataclass
class Recipient(ABC):
    """Recipient of a notification"""


@dataclass
class Message(ABC):
    """Notif message"""


class Notifier(ABC):
    """
    Base class for services that notify users in a standard way, regardless of the implemented platform. For the purpose
    of this exercise only email notifications are implemented, but one could feasibly build out SMS, Slack, voice call,
    or other such notification services with the same interface.
    """

    def notify(self, sender: Sender, recipient: Recipient, message: Message) -> NotifyResult:
        """Subclasses need to implement this, the "send a single notification" core method"""
        raise NotImplementedError('Concrete subclasses must implement this')
