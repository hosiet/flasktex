#!/usr/bin/env python3

"""
Testing Client for flasktex.
"""

__license__ = 'BSD-3'
__docformat__ = 'reStructuredText'


import urllib.request

def ft_checkalive(url:str):
    """
    Check whether given server is alive.
    """

    resp = None
    try:
        resp = urllib.request.urlopen(url+'/ping').read()
    except:
        return False
    if resp == b'pong':
        return True
    else:
        return False

def ft_test_client():
    url = input('flasktex url: ')
    url = url.rstrip('/')
    texdir = input('tex file dir: ')
    entryfile = input('entryfile filename: ')
    worker = input('worker name: ')
    timeout = input('timeout: ')

    print(' ** Checking Given Parameters...')
    print('checking server status...')
    if not ft_checkalive(url):
        print('Cannot connect to server. Giving up.')
        return
    print('pass', end='')
    print('checking local dir status...')
    dir_content = None
    try:
        dir_content = os.listdir(texdir)
    except:
        print('Error occurred when listing dir. Giving up.')
        return
    print('pass', end='')
    print('checking entryfile...')
    if not entryfile in dir_content:
        print('Cannot find given entryfile. Giving up.')
        return
    print('pass', end='')
    print('checking worker name...')
    print('skipped', end='')
    print('checking timeout value...')
    if int(timeout) < 30:
        print('Value too small. Giving up.')
        return
    print('pass', end='')
    print('\n...Success!')
    return {
        'url': str(url),
        'texdir': str(texdir),
        'entryfile': str(entryfile),
        'worker': str(worker),
        'timeout': int(timeout)
        }

def ft_client_submission(user_input):
    import flasktex
    from flasktex.tex2bundle import ft_dir_to_b64
    import flasktex.tex2bundle

    b64data = ft_dir_to_b64(user_input.texdir)
    json_str = flakstex.tex2bundle._ft_gen_texbundle_json_bundled(
            b64data,
            entryfile=user_input['entryfile'],
            worker=user_input['worker'],
            timeout=user_input['timeout'],
            )
    resp = urllib.request.urlopen(
            user_input['url'],
            data=json_str.encode('UTF-8'))
    return_data = resp.read()
    print(return_data)

    # TODO FIXME
    pass


if __name__ == '__main__':
    user_input = ft_test_client()
    if user_input:
        # TODO NEXT
        command = input('Submit? y/n: ')
        if command is '' or command is 'y':
            ft_client_submission(user_input)
        else:
            return
