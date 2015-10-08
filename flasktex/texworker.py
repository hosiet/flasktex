#!/usr/bin/env python3
#
# texworker.py -- background worker for flasktex
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
Background worker for latex
"""
import subprocess
import os, sys
import shutil
import signal
import sqlite3
import time
import syslog
from flasktex.config import ft_getconfig

# CONFIG
DEFAULT_RENDERER = ft_getconfig("DEFAULTRENDERER")
DEFAULT_TIMEOUT = ft_getconfig("WORKERTIMEOUT")
DATABASE_NAME = ft_getconfig("DATABASENAME")
DATABASE_PATH = ft_getconfig("DATABASEPATH")
assert DEFAULT_RENDERER
assert DEFAULT_TIMEOUT
assert DATABASE_NAME
assert DATABASE_PATH

class TexWorker():
    """
    A background worker to automatically finish the work.

    Will indeed daemonize by double-fork.
    Will end-up in given seconds.
    """
    def __init__(self, rawstring, renderer=DEFAULT_RENDERER,
                 timeout=DEFAULT_TIMEOUT, db=DATABASE_NAME,
                 path=DATABASE_PATH, args=None):
        self.rawstring = rawstring # Have to be UTF-8 String.
        assert hasattr(self.rawstring, 'encode')
        self.renderer = renderer
        self.timeout = int(timeout) # XXX: Have to be integer
        self.conn = sqlite3.connect(path+db)
        self.popen = None
        self.workid = None
        self.result = None
        c = self.conn.cursor()
        # Write to be in waiting line
        start_time = str(time.time())
        print('start_time is now {}.'.format(start_time))
        c.execute('INSERT INTO `work` VALUES (?,?,?,?,?,?,?,?);',
                (None, None, self.rawstring, None, start_time, None,
                    'R', None))
        self.conn.commit()
        found = False
        for i in c.execute('SELECT `id` FROM `work` WHERE starttime=?', (start_time,)):
            found = True
            self.workid = i[0];
            print('the workid is {}.'.format(self.workid))
            break
        if not found:
            raise Exception('WORKER_NOT_FOUND_IN_DATABASE')
        return

    def __startup(self):
        # Switch to working dir and make a subprocess.Popen object for working
        # After that, wait for timeout.
        syslog.syslog('at the beginning of __startup().')
        os.chdir("/tmp/")
        tempdir = None
        try:
            tempdir = subprocess.check_output(['mktemp', '-d', 'flasktex.XXXXXXXXXX'], timeout=2).decode('UTF-8').strip()
        except subprocess.TimeoutExpired:
            raise
        os.chdir("./{}/".format(tempdir))

        # Write input file as `input.tex'
        f = open('input.tex', 'wb')
        f.write(self.rawstring.encode('UTF-8'))
        f.close()
        syslog.syslog('after writing input.tex')

        # Form the Popen object, start the process, log in SQLite database
        try:
            self.popen = subprocess.Popen([self.renderer, '-no-shell-escape', '-halt-on-error', 'input.tex'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.conn.execute('UPDATE `work` SET `status`=? WHERE `id`={};'.format(self.workid), ('R',))
            self.conn.commit()
            syslog.syslog(str(e.args))
            syslog.syslog('after writing running state.')
            self.popen.wait(timeout=self.timeout)
            self.__terminate_handler(None, None)
        except Exception as e:
            syslog.syslog(str(e.args))

    def __cleanup(self, success=False):
        c = self.conn.cursor()
        c.execute('BEGIN TRANSACTION;')
        if success:
            # write pdf and status into database
            try:
                f = open('input.pdf', 'rb')
            except OSError:
                raise
            c.execute('UPDATE `work` SET `output`=?, `status`=? WHERE `id`={};'.format(self.workid),
                    (f.read(), 'S'))
            f.close()
        else:
            if self.popen.returncode == None:
                # terminate the Process first
                self.popen.terminate()
                self.result = 'X' # TIME_EXCEEDED
            else:
                self.result = 'E' # ERROR_HAPPENED
            c.execute('UPDATE `work` SET `status`=? WHERE `id`={};'.format(self.workid),
                    (self.result,))

        # write log and stoptime into database
        try:
            f = open('input.log', 'r')
        except OSError:
            raise
        c.execute('UPDATE `work` SET `log`=?, `stoptime`=? WHERE `id`={};'.format(self.workid),
                (f.read(), str(time.time())))

        # close database connection
        self.conn.commit()
        self.conn.close()
        # remove the temp dir
        cwd = os.getcwd()
        assert cwd.split('.')[0] == '/tmp/flasktex'
        os.chdir('..')
        shutil.rmtree(cwd)
        syslog.syslog('end of __cleanup(). status is {}.'.format(str(success)))
        return

    def __terminate_handler(self, signum, stackframe):
        syslog('entered handler with signum of {}.'.format(signum))
        signal.alarm(0)
        if self.popen == None or self.popen.returncode != 0:
            self.__cleanup(success=False)
            sys.exit(-1)
        else:
            self.__cleanup(success=True)
            sys.exit(0)

    def _do_work(self):
        """
        * Use SIGALRM to set timeout.

          If SIGALRM is received, consider that the worker
          is taking too much time, then gracefully exit and
          record the task as failed.
        """
        syslog.syslog('entering _do_work().')
        try:
            signal.signal(signal.SIGALRM, self.__terminate_handler)
            signal.signal(signal.SIGTERM, self.__terminate_handler)
            signal.alarm(self.timeout)
        except Exception as e:
            syslog.syslog(str(e.args))
        syslog.syslog('entering __startup().')
        self.__startup()
        signal.alarm(0)
        syslog.syslog('successfully finished the work within time.')
        self.__cleanup(success=True)

    def run(self): 
        # Daemonize and continue the work.
        try:
            syslog.syslog('before fork...')
            pid = os.fork()
            if pid > 0:
                # return to flask worker
                syslog.syslog('Parent process is returning...')
                return
        except OSError as e:
            syslog.syslog('OSError1!')
            raise
        os.chdir("/")
        os.setsid()
        os.umask(0)
        try:
            syslog.syslog('before second fork...')
            pid = os.fork()
            if pid > 0:
                syslog.syslog('second parent process is exiting...')
                sys.exit(0)
        except OSError as e:
            syslog.syslog('OSError1!')
            raise
        syslog.syslog('after second fork. continuing...')
        sys.stdout.flush()
        sys.stderr.flush()
        si = open("/dev/null", 'r')
        so = open("/dev/null", 'w')
        se = open("/dev/null", 'w')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # run the work.
        syslog.syslog('Will now begin the work.')
        self._do_work()

#  vim: set ts=8 sw=4 tw=0 et :
