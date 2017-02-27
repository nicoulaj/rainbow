# ----------------------------------------------------------------------
# rainbow, a command line colorizer
# Copyright (C) 2011-2017 Julien Nicoulaud <julien.nicoulaud@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import os
import signal
from threading import Timer
from time import sleep

import pytest

from rainbow.runner import CommandRunner
from rainbow.runner import STDINRunner


@pytest.mark.timeout(5)
def test_005_command_line_runner_interrupted():
    Timer(0.5, os.kill, [os.getpid(), signal.SIGINT]).start()
    assert CommandRunner(['sleep', '100']).run() == -2


@pytest.mark.timeout(5)
def test_006_stdin_runner_interrupted():
    Timer(0.5, os.kill, [os.getpid(), signal.SIGINT]).start()
    assert STDINRunner(input_=lambda: sleep(100)).run() == 1
