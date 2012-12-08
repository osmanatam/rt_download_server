#!/usr/bin/env python

'''Module for inner torrent downloader server authentification'''

import hashlib
import platform
import time
import datetime
import hmac

def _get_system_salt():
    '''Returns system specific string for salting hash.'''

    return platform.processor()

_salt = ('028572', _get_system_salt())

users = {}   # global mapping username -> password hash
cookies = {} # cookie string and expiration time

def make_passwd_hash(passwd):
    '''Makes hash of password for inner torrent download server use.'''

    h = hashlib.sha256()
    h.update(passwd)
    for s in _salt:
        h.update(s)

    return h.digest()

def add_user(uname, passwd):
    '''Adds user to global mapping of torrent download server users.'''

    if uname in users:
        raise RuntimeError('user \'%s\' already exists')

    users[uname] = make_passwd_hash(passwd)

def check_user(uname, passwd):
    '''Returns True if user if 'uname' exists and its passowrd is 'passwd'.'''

    return uname in users and users[uname] == make_passwd_hash(passwd)

def make_cookie(uname):
    '''Retuns tuple of cookie for specified user and it expiration datetime.'''

    cookie = hmac.new(str(time.time()) + uname).hexdigest()

    expires = datetime.datetime.now() + datetime.timedelta(minutes=30)
    cookies[cookie] = expires

    return (cookie, expires)

def is_good_cookie(cookie):
    '''Returns True if cookie exists and not expired.'''

    return cookie in cookies and datetime.datetime.now() <= cookies[cookie]

