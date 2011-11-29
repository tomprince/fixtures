#  fixtures: Fixtures with cleanups for testing and convenience.
#
# Copyright (C) 2011, Martin Pool <mbp@sourcefrog.net>
# 
# Licensed under either the Apache License, Version 2.0 or the BSD 3-clause
# license at the users choice. A copy of both licenses are available in the
# project source as Apache-2.0 and BSD. You may not use this file except in
# compliance with one of these two licences.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under these licenses is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# license you chose for the specific language governing permissions and
# limitations under that license.


import signal

import fixtures


class TestTimeoutException(Exception):
    """Test timed out"""


class Timeout(fixtures.Fixture):

    def __init__(self, timeout_secs, gentle):
        self.timeout_secs = timeout_secs
        self.alarm_fn = getattr(signal, 'alarm', None)
        self.gentle = gentle

    def signal_handler(self):
        raise TestTimeoutException()

    def setUp(self):
        super(TestTimeout, self).setUp()
        if self.alarm_fn is None:
            return  # Can't run on Windows
        self.alarm_fn(self.timeout_secs)
        self.addCleanup(lambda: self.alarm_fn(0))
        if self.gentle:
            saved_handler = signal.signal(signal.SIGALRM, self.signal_handler)
            self.addCleanup(lambda: signal.signal(signal.SIGALRM, saved_handler))
            # Otherwise, the SIGALRM will probably kill the process.
