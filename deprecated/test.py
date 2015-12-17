#!/usr/bin/python3
import flasktex
f=open('testing.tex', 'r')
s=f.read()
f.close()
worker = flasktex.texworker.TexWorker(s, renderer='pdflatex', timeout=60)
worker._do_work()
