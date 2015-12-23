#!/usr/bin/env python3

from flasktex.texrequest import TeXRequest


FT_WORKER_DEFAULT = 'xelatex'
FT_TIMEOUT_DEFAULT = 60
FT_ENTRYFILE_DEFAULT = 'main.tex'


def ft_xmlbundle_to_request(xmlbundle) -> TeXRequest:
    """
    Convert xmlbundle to standard process request.

    xmlbundle should be str-typed.

    return: flasktex.TeXRequest instance.
    """
    import xml
    import xml.dom as dom
    import xml.dom.minidom as minidom
    import base64

    worker = FT_WORKER_DEFAULT
    timeout = FT_TIMEOUT_DEFAULT  # FIXME: set default in config file
    entryfile = FT_ENTRYFILE_DEFAULT

    # XXX: Use ElementTree instead of DOM
    doc = minidom.parseString(xmlbundle)
    rootElement = doc.documentElement
    assert rootElement.tagName == 'xmlbundle'
    assert len([x for x in rootElement.childNodes if x.tagName == 'bundle']) == 1
    reqList = [x for x in rootElement.childNodes if x.tagName == 'request']
    if len(reqList) == 1:
        requestElement = reqList[0]
        if requestElement.getElementsByTagName('worker') != []:
            worker = requestElement.getElementsByTagName('worker')[0].firstChild.nodeValue
        if requestElement.getElementsByTagName('timeout') != []:
            timeout = int(requestElement.getElementsByTagName('timeout')[0].firstChild.nodeValue)
        if requestElement.getElementsByTagName('entryfile') != []:
            entryfile = requestElement.getElementsByTagName('entryfile')[0].firstChild.nodeValue
    targz_data = base64.b64decode(
            [x for x in rootElement.childNodes if x.tagName == 'bundle'][0].firstChild.nodeValue,
            validate=True
            )
    texrequest =TeXRequest(targz_data, worker=worker, timeout=timeout, entryfile=entryfile)
    return texrequest


def ft_json_to_request(jsondata) -> TeXRequest:
    """Convert json submitted data into texrequest.
    """
    return None
