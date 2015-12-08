"""Define tex request class.
"""
class TeXRequest():

    def set_status(self, status_str: str):
        self.__status = status_str
        return

    def get_status(self):
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
        self.targz_data = targz_data
        self.worker = worker
        self.timeout = timeout
        self.entryfile = entryfile
        self.set_status('INIT')

    def process(self):
        if self.get_status() != 'INIT': # already started
            return (False, 'ERR_ALREADY_STARTED')
        self.set_status('STARTING')
        pass

