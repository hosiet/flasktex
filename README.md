# flasktex
- Compile and get PDF online by Flask and (Xe)LaTeX

## Usage

Read the code for details.

### Flask routes

#### `/about`

Show the about page.

#### `/api/status`

Show all status of all the works.

#### `/api/submit` (POST)

Post the plain text as LaTeX source and start the work.

#### `/api/obtain/<number>.pdf`

Get the output pdf, if finished.

### Start up

#### Run as python module
Simply run `import flasktex`

#### Run as standalone HTTP Server for debug
`python3 debug.py`

#### Run with uwsgi support
set module to mainapp and runnable to `app`.

## Useful latex arguments

* `halt-on-error` Exit with error code immediately after error happened.

* * *

## LICENSE

3-clause BSD

------------------------

```
Copyright (c) 2015, Boyuan Yang <073plan@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
