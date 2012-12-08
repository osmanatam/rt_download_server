#!/usr/bin/env python

'''Module contains TAuthHandler class for handling own torrent add server
authentification.
'''

import tanyhandler
import auth

class TAuthHandler(tanyhandler.IHandler):
    '''Class for handling inner authentification in download server.


    It should be in page_template.auth_path in handlers dictionary.
    '''

    def process(self, body=None, browser=None):
        '''Checks if user entered correct password and answers.

        body parameter is used to get 'uname' and 'password'.
        If data is correct, user gets cookie, HTTP 401 otherwise.
        '''

        if not auth.check_user(body['uname'], body['passwd']):
            status = 401
            return status, None, None

        (cookie, expires) = auth.make_cookie(body['uname'])

        status = 301
        headers = {
            'Set-Cookie': 'ID=%s ; expires=%s' % (cookie, expires.strftime('%a, %d %b %Y %H:%M:%S GMT')),
            'Location': '/'
        }

        return status, headers, None

