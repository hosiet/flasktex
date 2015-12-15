"""Define tex request class.
"""

import flasktex.db
import sqlite3
import os, sys, signal, syslog
import tempfile, tarfile

class TeXRequest():

    @staticmethod
    def daemonize():
        """Daemonize with special treatments.

        Note: Please, manually ensure that database connection
        is closed before. You need to re-connect to the database
        afterwards.

        If return False, we are still in original process.
        If return True, we are in daemon process.
        """
        syslog.syslog('Begin Daemonize...')
        try:
            pid = os.fork()
            if pid > 0:
                return False # return to Flask process
        except OSError as e:
            syslog.syslog('OSError1! {}'.format(str(e)))
            raise
        os.chdir("/")
        os.setsid()
        os.umask(0)
        sys.stdout.flush()
        sys.stderr.flush()

        # Close all open file descriptors
        MAXFD = os.sysconf("SC_OPEN_MAX")
        for i in range(0, MAXFD):
            try:
                os.close(i)
            except:
                pass

        # Second Fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            syslog.syslog('OSError2: {}'.format(e))
            raise
        si = open("/dev/null", 'r')
        so = open("/dev/null", 'w')
        se = open("/dev/null", 'w')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        syslog.syslog('daemonize finished, pid is {}.'.format(os.getpid()))
        return True

    def _reopen_db_conn(self):
        if self.conn != None:
            try:
                self.conn.close()
            except:
                pass
            self.conn = None
        self.conn = flasktex.db.ft_db_init_conn()
        return self.conn

    def set_status(self, status_str: str):
        flasktex.db.ft_db_record_set_status(self.conn, self.id, status_str)
        self.__status = status_str
        return

    def get_status(self):
        # TODO OBTAIN STATUS FROM DB
        self.__status = flasktex.db.ft_db_record_get_status(self.conn, self.id)
        return self.__status

    def is_successful(self):
        pass


    def __init__(
                self,
                targz_data: bytes,
                worker: str = "xelatex",
                timeout: int = 60,
                entryfile: str = "main.tex",
            ):
        """Init the object.

        Meanwhile, write into the database.

        If success, work ID will be set. Otherwise raise an exception.
        """

        self.targz_data = targz_data
        self.worker = worker
        self.timeout = timeout
        self.entryfile = entryfile
        self.conn = None;
        # Open Database Connection
        self._reopen_db_conn();
        assert self.conn != None
        # Write initial information into database
        self.id = flasktex.db.ft_db_setup_record(self, self.conn)
        assert type(self.id) == type(1)
        self.__status = 'INIT'
        return

    def process(self):
        """Start the job.

        Note that the worker will be started with double-fork magic
        to become an independent process.

        uwsgi-side will return immediately with (True, ""), while worker-side
        will finish the work, write the database and self-suiside.

        The detailed work is as follows:
         1.  daemonize
         2.  obtain tempdir
         3.  check and extract full data
         4.  call subprocess, await finish
         5.  check status, write pdf and log into database
         6.  clean tempdir
         7.  terminate
        """

        # Set status to 'STARTING'
        if self.get_status() != 'INIT': # already started
            return (False, 'ERR_ALREADY_STARTED')
        self.set_status('STARTING')

        #1: Daemonize
        self.conn.close()
        self.conn = None
        result = self.daemonize()
        if result == False: # Not forked
            self._reopen_db_conn()
            return (True, '')
        # We are in daemon now, continue
        self._reopen_db_conn()

        #2: obtain tempdir
        with tempfile.TemporaryDirectory(prefix='flasktex.') as tmpdirname:
            # WARNING: Python 3.2+ only
            fileobj = tempfile.SpooledTemporaryFile(mode="w+b")
            fileobj.write(self.targz_data)
            fileobj.seek(0)
            tar = tarfile.open(mode="r:gz", format=tarfile.PAX_FORMAT, fileobj = fileobj)
            tar.extractall(path=tmpdirname+"/.")

        # TODO FIXME

        pass

