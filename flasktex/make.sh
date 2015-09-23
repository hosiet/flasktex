#!/bin/sh
#
# Shell script used to make latex pdf.
#
# Usage:
#
# make.sh [latex-program-name] [timeout] [input-filename]
#
# shall always rename input filename to input.tex and output
# should also be input.pdf, with input.log, input.aux.

set -e
FLASKTEX_LATEX_PROG_NAME=$1
FLASKTEX_TIMEOUT=$2
FLASKTEX_FILENAME=$3

# Make assertions
#
# TODO FIXME
# assert pwd is made by mktemp in /tmp/flasktex/

mv $FLASKTEX_FILENAME input.tex
timeout "$FLASKTEX_TIMEOUT" "$FLASKTEX_LATEX_PROG_NAME" -no-shell-escape -halt-on-error ./input.tex > /dev/null 2> /dev/null < /dev/null
