from abc import ABC
from dataclasses import dataclass


@dataclass
class Sender(ABC):
    """Sender of a notification"""


@dataclass
class Recipient(ABC):
    """Recipient of a notification"""


@dataclass
class Message(ABC):
    """Notif message"""

