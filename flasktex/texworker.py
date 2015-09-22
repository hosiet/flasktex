#!/usr/bin/env python3
"""
Background worker for latex

Interfaces
==========

.run()    run as standalone.
          will self-destruct after given timeout.
"""
import subprocess

# CONFIG
DEFAULT_RENDERER = ft_getconfig("DEFAULTRENDERER")
assert DEFAULT_RENDERER

class TexWorker():
    def __init__(self, rawstring, renderer=DEFAULT_RENDERER, args=None):
        pass
#  vim: set ts=8 sw=4 tw=0 et :
