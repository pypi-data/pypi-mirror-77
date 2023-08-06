# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import gevent
import gevent.queue

from wampy.errors import WampyTimeOutError
from wampy.interfaces import Async


class Gevent(Async):

    def __init__(self, message_queue=gevent.queue.Queue()):
        self.message_queue = message_queue

    def __str__(self):
        return 'GeventAsyncAdapter'

    def queue(self):
        # TODO: why?
        return gevent.queue.Queue()

    def Timeout(self, timeout, raise_after=True):
        return gevent.Timeout(timeout, raise_after)

    @property
    def QueueEmpty(self):
        return gevent.queue.Empty

    def receive_message(self, timeout):
        try:
            message = self._wait_for_message(timeout)
        except gevent.Timeout:
            raise WampyTimeOutError(
                "no message returned (timed-out in {})".format(timeout)
            )
        return message

    def spawn(self, *args, **kwargs):
        gthread = gevent.spawn(*args, **kwargs)
        return gthread

    def sleep(self, time=0):
        gevent.sleep(time)

    def _wait_for_message(self, timeout):
        # executed every time a Client expects to recieve a Message
        q = self.message_queue

        with gevent.Timeout(timeout):
            while q.qsize() == 0:
                gevent.sleep()

        message = q.get()
        return message
