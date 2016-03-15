#!/usr/bin/env python3

class UploadedWorkRequest(object):
    """
    Object contains the POSTed json/xml request.

    """
    def __init__(self, uploaded_data: dict, objtype = 'json'):
        super().__init__()
        if objtype is 'xml':
            raise NotImplementedError
        for i in uploaded_data:
            assert isinstance(i, str)
            setattr(self, i, uploaded_data[i])

