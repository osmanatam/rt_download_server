#!/usr/bin/env python

import sys
import getpass
import tserv
import rt_browser
import tanyhandler
import tauthhandler
import taddhandler
import page_template
import BaseHTTPServer as bhs
import functools
import ConfigParser
import getopt
import os.path

import auth

def _usage(progname):
    print '''Usage: %s -c config [-p port] [-h] [--help]
    Starts server for downloading .torrent files from
    RuTracker.Org and starting torrent download.

    -c, --config= config - path to server config
    -p, --port= port - overrides config's port value
    -h, --help - print this help and exit
    '''

def get_rutracker_authdata():
    print 'Please enter RuTracker.Org login data'
    print 'login: ',
    sys.stdout.flush()

    login = sys.stdin.readline().strip()

    password = getpass.getpass('password: ')

    return (login, password)


def parse_args(args):
    '''Parses command line arguments.'''

    (opts, args) = getopt.getopt(args, 'c:p:h', ['help', 'config=', 'port='])

    if len(args):
        _usage(sys.argv[0])
        sys.exit(1)

    conffile = None
    port = None

    for (opt, arg) in opts:
        if opt in ('-c', '--config'):
            conffile = arg
        elif opt in ('-p', '--port'):
            port = arg
        else:
            _usage(sys.argv[0])
            sys.exit(1)

    if not conffile:
        _usage(sys.argv[0])
        sys.exit(1)

    return (conffile, port)

def parse_conf(conffile):
    '''Parses config file.'''

    parser = ConfigParser.RawConfigParser()
    parser.read(conffile)

    port, save_path = (None, None)
    try:
        port = parser.getint('Server', 'port')
        save_path = parser.get('Server', 'save_path')
    except ConfigParser.Error:
        pass

    users = parser.items('Users')

    return port, save_path, users

if __name__ == '__main__':
    (conffile, argport) = parse_args(sys.argv[1:])

    (port, save_path, users) = parse_conf(conffile)
    if argport:
        port = argport

    if not len(users):
        print 'Error: no users in %s config file' % conffile
        sys.exit(1)

    for (user, passwd) in users:
        auth.add_user(user, passwd)

    add_handler = taddhandler.TAddHandler(page_template.success)
    if save_path:
        add_handler.set_save_path(os.path.expanduser(save_path))
    add_handler.set_file_exists_template(page_template.file_exists)

    handlers = {
        '*': tanyhandler.TAnyHandler(page_template.index),
        'auth': tauthhandler.TAuthHandler(''),
        'torrentadd': add_handler
    }

    (login, password) = get_rutracker_authdata()

    browser = rt_browser.RutrackerBrowser(login, password)
    browser.login()

    addr = ('', port)
    serv = bhs.HTTPServer(
            addr,
            functools.partial(tserv.TorrentServHandler, handlers, browser)
    )
    serv.serve_forever()


    sys.exit(0)

