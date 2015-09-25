#!/usr/bin/python3

# Script for uwsgi to start.

import flasktex

# Won't run
app = flasktex.app
app.run(debug=True)

#  vim: set ts=8 sw=4 tw=0 et :
