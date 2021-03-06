#!/usr/bin/env python3
#
# flasktexd.py -- standalone daemon for background processing
#
# This file is part of flasktex.
#
# Copyright (c) 2015, Boyuan Yang <073plan@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Standalone Daemon for Flasktex
"""
import os, sys
import daemon
import flasktex
import syslog

def ft_daemon_startup():
    """
    Entry point for flasktexd daemon.

    Daemonize would preserve stdout and stderr to work with systemd.
    """
    print(sys.argv)
    print(flasktex.__version__)
    syslog.syslog('I will be a daemon.')
    with daemon.DaemonContext(
            stdout=sys.stdout,
            stderr=sys.stderr,
        ):
        syslog.syslog('I am a daemon now.')
    syslog.syslog('I am leaving.')

def ft_daemon_mainloop():
    """
    Main Loop for processing.

    Consider using:
    * `/var/spool/flasktex/` for job queue
    * `/var/run/flasktex/` for daemon lock and wakeup pipe

    In the spool directory, all the jobs should be named as
    `$UNIX_TIME.$MILLISECOND` so as to be recognized properly.
    the standard version is the output of time.time().

    """
    # TODO: use var to replace hardcoded path for flexibility

if __name__ == "__main__":
    ft_daemon_startup()
    pass

#  vim: set ts=8 sw=4 tw=0 et :
