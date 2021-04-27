from dataclasses import dataclass

from app.service.notification import Recipient, Sender, Message


@dataclass
class EmailAddressee(Sender, Recipient):
    name: str

    """Email address"""
    email: str


@dataclass
class EmailMessage(Message):
    subject: str
    body: str
