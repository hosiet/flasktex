#!/usr/bin/env python3

from flasktex.texrequest import TeXRequest


def ft_xmlbundle_to_request(xmlbundle) -> TeXRequest:
    """Put xmlbundle to standard process request.
    
    xmlbundle should be str-typed.

    return: flasktex.TeXRequest instance.
    """
    import xml
    import xml.dom as dom
    import xml.dom.minidom as minidom
    import base64

    worker = 'xelatex'
    timeout = 60 # FIXME: set default in config file
    entryfile = 'main.tex'

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

