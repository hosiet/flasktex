#!/usr/bin/env python3
"""make files in given dir into xml bundle string.
"""

__license__ = 'BSD-3'
__docformat__ = 'reStructuredText'

import sys
import os
import xml
import xml.dom as dom

def ft_dir_to_b64(path:str) -> bytes:
    """
    Convert the given directory to a targz file, then base64 it.

    :param arg1: the directory path
    :type arg1: str
    :returns: the base64-encoded bytes
    :rtype: bytes

    ..note:: Even though we prefer POSIX.1-2001(pax) formatted farfile,
        the whole program will still support GNU tar format.
    ..todo:: any kind of improvement is welcomed.
    """
    import tarfile
    import tempfile
    import base64

    pwd = os.getcwd()
    fileobj = tempfile.SpooledTemporaryFile(mode='w+b')
    tar = tarfile.open(mode="w:gz", format=tarfile.PAX_FORMAT, fileobj=fileobj)
    os.chdir(path)
    tar.add(".")
    os.chdir(pwd)
    tar.close()
    fileobj.seek(0)

    return base64.b64encode(fileobj.read())


def _ft_gen_texbundle_xml(
        b64bytes:bytes,
        entryfile="main.tex",
        worker='xelatex',
        timeout=60) -> str:
    """
    Generate xmlbundle from base64 bytes and given metadata as api_1_0.

    :returns: XML-formatted bundle string
    :rtype: str
    """

    impl = dom.getDOMImplementation()
    doc = impl.createDocument(None, "xmlbundle", None)
    reqNode = doc.createElement('request')
    workerNode = doc.createElement('worker')
    workerNode.appendChild(doc.createTextNode(worker))
    reqNode.appendChild(workerNode)
    timeoutNode = doc.createElement('timeout')
    timeoutNode.appendChild(doc.createTextNode(str(timeout)))
    reqNode.appendChild(timeoutNode)
    entryNode = doc.createElement('entryfile')
    entryNode.appendChild(doc.createTextNode(str(entryfile)))
    reqNode.appendChild(entryNode)
    doc.documentElement.appendChild(reqNode)
    bundleNode = doc.createElement('bundle')
    bundleNode.appendChild(doc.createTextNode(b64bytes.decode('UTF-8')))
    doc.documentElement.appendChild(bundleNode)

    return doc.toxml()

def _ft_gen_texbundle_json_bundled(
        b64bytes:bytes,
        entryfile='main.tex',
        worker='xelatex',
        timeout=60) -> str:
    """
    Generate json bundle (bundled style) from base64 bytes and given metadata
    as api_1_0.

    Written to use json.dumps()

    :returns: JSON-formatted bundle string
    :rtype: str
    """

    import json

    return json.dumps(
        dict(
            request=dict(
                worker=worker,
                timeout=timeout, 
                entryfile=entryfile,
                ),
            type='bundle',
            content=dict(
                content_type='base64',
                content=b64bytes.decode('UTF-8'),
                ),
            )
        )



if __name__ == "__main__":
    if not len(sys.argv) == 2:
        os.abort()
    mybytes = ft_dir_to_b64(sys.argv[1])
    myxml = _ft_gen_texbundle_xml(mybytes)
    print(myxml)
