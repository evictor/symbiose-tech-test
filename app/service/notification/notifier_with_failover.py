from itertools import cycle
from typing import List, Optional

from app.service.notification import Notifier, Recipient, NotifyResult, Sender, Message


class NotifierWithFailover(Notifier):
    """
    When sending a notif, selects a notifier from a preset list of notifiers to make the notify attempt. If the
    selected notifier fails, an attempt is made to send the notif with the next notifier in the list, and so on until
    a successful send, or the list is exhausted with each notifier having failed in succession (in which case the notify
    call itself fails with the last failure result). If one notifier succeeds before the list is exhausted, that success
    result is returned, and the notifier that was successful becomes the current de facto "active" notifier, i.e. to be
    selected first to attempt sending a notif during a subsequent call to notify.

    The algo as described is effectively an auto-failing over notification scheme that handles service outages and will
    not repeatedly attempt to use services that previously failed. That is, a previously failed notifier will only be
    attempted once again when all other notifiers have also failed, *and* the attempt is part of a distinct notify call
    (i.e. a given notifier will not be attempted more than once per notify call).
    """

    """The list of notifiers in order of selection for the algo described in the class doc str"""
    _notifiers: List[Notifier]

    """Number of _notifiers; used to detect when _notifier_it has looped"""
    _num_notifiers: int

    """Infinitely looping iterator over __notifiers"""
    _notifier_it: cycle

    """
    Current "active" notifier, i.e. the last one to succeed, or simply the first in _notifiers, as in the case that no
    calls to notify have been made (no notifiers have been attempted yet)
    """
    _notifier: Notifier

    def __init__(self, notifiers: List[Notifier]):
        """
        :param notifiers: List of notifier services to consider for the algo described in the class doc str. The given
                          order is the order in which notifier services will be attempted given a start index in the
                          list equal to the most recently succeeded notifier. A copy of the list will be made so that
                          mutations to the original will not affect this instance.
        """
        self._notifiers = [*notifiers]
        self._num_notifiers = len(notifiers)
        if self._num_notifiers == 0:
            raise ValueError('Expected at least 1 notifier in param `notifiers`')

        # An iterator that loops over the notifiers indefinitely
        self._notifier_it = cycle(self._notifiers)
        self._notifier = next(self._notifier_it)

    def notify(self, sender: Sender, recipient: Recipient, message: Message) -> NotifyResult:
        result: Optional[NotifyResult] = None
        num_notif_attempts = 0

        def did_succeed() -> bool:
            return result is not None and result.success

        # Attempt notif at most once per notifier before aborting
        while not did_succeed() and num_notif_attempts < self._num_notifiers:
            num_notif_attempts += 1
            result = self._notifier.notify(sender, recipient, message)
            if not result.success:
                self._notifier = next(self._notifier_it)

        result.num_notifiers_attempted = num_notif_attempts
        return result
