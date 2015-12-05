#!/usr/bin/python3

# For standalone daemon or uwsgi use.

import flasktex

app = flasktex.app

if __name__ == '__main__':
    app.run(debug=True)

#  vim: set ts=8 sw=4 tw=0 et :
