#!/usr/bin/python3
import os
os.chdir('..')
print(os.getcwd())
import flasktex
os.chdir('flasktex')
import texworker
f=open('testing.tex', 'r')
s=f.read()
f.close()
worker = texworker.TexWorker(s, renderer='pdflatex', timeout=60)
worker._do_work()
