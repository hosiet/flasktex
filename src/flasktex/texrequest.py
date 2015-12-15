"""Define tex request class.
"""

import flasktex.db
import sqlite3

class TeXRequest():

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
        self.__status = status_str
        # TODO SYNC STATUS WITH 
        return

    def get_status(self):
        # TODO OBTAIN STATUS FROM DB
        return self.__status

    def is_successful(self):
        pass


    def __init__(
        """Init the object.

        Meanwhile, write into the database.

        If success, work ID will be set. Otherwise raise an exception.
        """
                self,
                targz_data: bytes,
                worker: str = "xelatex",
                timeout: int = 60,
                entryfile: str = "main.tex",
            ):
        def _get_new_id(conn):
        self.targz_data = targz_data
        self.worker = worker
        self.timeout = timeout
        self.entryfile = entryfile
        self.conn = None;
        self._reopen_db_conn();
        self.id = flasktex.db.ft_db_setup_record(self, self.conn)
        #self.set_status('INIT') # NOT NEEDED

    def process(self):
        if self.get_status() != 'INIT': # already started
            return (False, 'ERR_ALREADY_STARTED')
        self.set_status('STARTING')
        pass

