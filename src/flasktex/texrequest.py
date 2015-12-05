"""Define tex request class.
"""
class TeXRequest():

    def set_status(self, status_str):
        pass

    def get_status(self):
        pass

    def is_successful(self):
        pass

    def __init__(self, targz_data: bytes, worker="xelatex", timeout=60):
        self.targz_data = targz_data
        self.worker = worker
        self.timeout = timeout
        self.entryfile = entryfile
        self.set_status('INIT')

    def process(self):
        pass

