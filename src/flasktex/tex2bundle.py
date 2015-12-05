#!/usr/bin/env python3
"""make files in given dir into xml bundle string.
"""

import sys, os
import xml
import xml.dom as dom

def ft_dir_to_b64(path):
    """gzip given dir, then base64 it.

    return the base64-encoded bytes.
    """
    import tarfile, tempfile, base64

    fileobj = tempfile.SpooledTemporaryFile(mode='w+b')
    tar = tarfile.open(mode="w:gz", fileobj=fileobj)
    tar.add(path)
    tar.close()
    fileobj.seek(0)

    return base64.b64encode(fileobj.read())

def _ft_gen_texbundle_xml(b64bytes, entryfile="main.tex", worker='xelatex', timeout=60):
    """Generate xmlbundle as in api v1.0.

    return str object.
    """
    import xml
    import xml.dom as dom

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

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        os.abort()
    mybytes = ft_dir_to_b64(sys.argv[1])
    myxml = _ft_gen_texbundle_xml(mybytes)
    print(myxml)
