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
        if self.get_status() != 'INIT': # already started
            return (False, 'ERR_ALREADY_STARTED')
        self.set_status('STARTING')
        pass

