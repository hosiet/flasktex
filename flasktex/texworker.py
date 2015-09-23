#!/usr/bin/env python3
"""
Background worker for latex
"""
import subprocess
import os, sys
import shutil
import signal

# CONFIG
DEFAULT_RENDERER = ft_getconfig("DEFAULTRENDERER")
DEFAULT_TIMEOUT = ft_getconfig("WORKERTIMEOUT")
assert DEFAULT_RENDERER
assert DEFAULT_TIMEOUT

class TexWorker():
    """
    A background worker to automatically finish the work.

    Will indeed daemonize by double-fork.
    Will end-up in given seconds.
    """
    def __init__(self, rawstring, renderer=DEFAULT_RENDERER, timeout=DEFAULT_TIMEOUT, args=None):
        self.rawstring = rawstring # Have to be UTF-8 String.
        assert hasattr(self.rawstring, 'encode')
        self.renderer = renderer
        self.timeout = timeout
        self.popen = None
        self.result = None
        pass

    def __startup(self):
        # TODO
        # Switch to working dir and make a subprocess.Popen object for working
        # After that, wait for timeout.
        try:
            os.chdir("/tmp/")
            tempdir = None
            try:
                tempdir = subprocess.check_output(['mktemp', '-d', 'flasktex.XXXXXXXXXX'], timeout=2) # 10 X
            except subprocess.TimeoutExpired:
                raise
            os.chdir("./{}/".format(tempdir))
        except OSError:
            raise

        # Write input file as `input.tex'
        f = file('input.tex', 'wb')
        f.write(self.rawstring.encode('UTF-8'))
        f.close()

        # Form the Popen object, start the process, log in SQLite database
        self.popen = subprocess.Popen([self.renderer, '-no-shell-escape', '-halt-on-error', 'input.tex'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # TODO LOGGING
        self.popen.wait(timeout=self.timeout)
        self.__terminate_handler(None, None)
        pass

    def __cleanup(self, success=False):
        # TODO
        # TODO Write the database!
        if success:
            pass
        else:
            if self.popen.returncode == None:
                # terminate the Process first
                self.popen.terminate()
                self.result = 'E'

        # remove the temp dir
        cwd = os.getcwd()
        assert cwd.split('.')[0] == '/tmp/flasktex'
        os.chdir('..')
        shutil.rmtree(cwd)


        pass

    def __terminate_handler(self, signum, stackframe):
        if self.popen == None or self.popen.returncode != 0:
            self.cleanup(success=False)
            sys.exit(-1)
        else:
            self.cleanup(success=True)
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
        except OSError, e:
            raise
        os.chdir("/")
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            raise
        sys.stdout.flush()
        sys.stderr.flush()
        si = file("/dev/null", 'r')
        so = file("/dev/null", 'a+')
        se = file("/dev/null", 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # run the work.
        self._do_work()

#  vim: set ts=8 sw=4 tw=0 et :
