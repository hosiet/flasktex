#!/usr/bin/env python3
"""
Background worker for latex
"""
import subprocess
import os, sys
import shutil
import signal
import sqlite3
import time

from flasktex.config import ft_getconfig

# CONFIG
DEFAULT_RENDERER = ft_getconfig("DEFAULTRENDERER")
DEFAULT_TIMEOUT = ft_getconfig("WORKERTIMEOUT")
DATABASE_NAME = ft_getconfig("DATABASENAME")
assert DEFAULT_RENDERER
assert DEFAULT_TIMEOUT
assert DATABASE_NAME

class TexWorker():
    """
    A background worker to automatically finish the work.

    Will indeed daemonize by double-fork.
    Will end-up in given seconds.
    """
    def __init__(self, rawstring, renderer=DEFAULT_RENDERER,
                 timeout=DEFAULT_TIMEOUT, db=DATABASE_NAME, args=None):
        self.rawstring = rawstring # Have to be UTF-8 String.
        assert hasattr(self.rawstring, 'encode')
        self.renderer = renderer
        self.timeout = timeout
        self.conn = sqlite3.connect(db)
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
        os.chdir("/tmp/")
        tempdir = None
        try:
            tempdir = subprocess.check_output(['mktemp', '-d', 'flasktex.XXXXXXXXXX'], timeout=2).decode('UTF-8').strip()
        except subprocess.TimeoutExpired:
            raise
        os.chdir("./{}/".format(tempdir))
        print('now pwd is {}.'.format(os.getcwd())) # DEBUG

        # Write input file as `input.tex'
        f = open('input.tex', 'wb')
        f.write(self.rawstring.encode('UTF-8'))
        f.close()
        print('input.tex File written.') # DEBUG

        # Form the Popen object, start the process, log in SQLite database
        self.popen = subprocess.Popen([self.renderer, '-no-shell-escape', '-halt-on-error', 'input.tex'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.conn.execute('UPDATE `work` SET `status`=? WHERE `id`={};'.format(self.workid), ('R',))
        self.conn.commit()
        print('Will now wait for subprocess to terminate.')
        self.popen.wait(timeout=self.timeout)
        self.__terminate_handler(None, None)
        pass

    def __cleanup(self, success=False):
        print('Beginning cleanup. result:{}.'.format(str(success))) # DEBUG
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
        print('pwd is {}.'.format(os.getcwd()))
        assert cwd.split('.')[0] == '/tmp/flasktex'
        os.chdir('..')
        print('pwd is {}.'.format(os.getcwd()))
        os.system('ls')
        shutil.rmtree(cwd)
        os.system('ls')
        return

    def __terminate_handler(self, signum, stackframe):
        print('Now inside signal handler.')
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
        signal.signal(signal.SIGALRM, self.__terminate_handler)
        signal.signal(signal.SIGTERM, self.__terminate_handler)
        signal.alarm(self.timeout)
        self.__startup()
        signal.alarm(0)
        self.__cleanup(success=True)

    def run(self): 
        # Daemonize and continue the work.
        try:
            pid = os.fork()
            if pid > 0:
                # return to flask worker
                return
        except OSError as e:
            raise
        os.chdir("/")
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            raise
        sys.stdout.flush()
        sys.stderr.flush()
        si = open("/dev/null", 'r')
        so = open("/dev/null", 'w')
        se = open("/dev/null", 'w')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # run the work.
        self._do_work()

#  vim: set ts=8 sw=4 tw=0 et :
