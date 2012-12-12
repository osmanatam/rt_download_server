#!/usr/bin/env python

'''Module with class holding Server's config.'''

import ConfigParser
import os.path

class TorrentDownloaderConfig(object):
    '''Class holding server's config.

    Some useful fields:
    port - server port
    save_path - path to put .torrent files to
    self.users - list of (user, password) pairs.
    '''

    def __init__(self, filename):
        '''Takes config filename as parameter, initialises own fields.'''

        self.parser = ConfigParser.RawConfigParser()
        self.parser.read(filename)

        self.port = self._get_int('Server', 'port', default=80)
        self.save_path = self._get_path('Server', 'save_path')

        self.users = self.parser.items('Users')


    def _get_int(self, section, option, default=0):
        '''Gets int number from config.'''

        try:
            return self.parser.getint(section, option)
        except ConfigParser.Error:
            return default


    def _get_path(self, section, option, default='.'):
        '''Gets path from config.'''

        path = default
        try:
            path = self.parser.get(section, option)
        except ConfigParser.Error:
            pass

        path = os.path.expanduser(path)

        if not os.path.exists(path):
            raise RuntimeError('path does not exists')

        return path


