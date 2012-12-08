#!/usr/bin/env python

'''Handler for adding torrent in torrent download server'''

import tanyhandler
import urllib
import os.path

class TAddHandler(tanyhandler.IHandler):
    '''Class handles download of torrents for torrent download server.

    Can be configured with save path - where to save .torrent files and
    file_exists_template - page template for reporting attempts to overwrite
    existing file.
    '''

    def __init__(self, page_template):
        '''Takes page_template for succesful requests (as parent class).

        Addidtionally sets own save path as current working directory and
        sets own primitive file_exists_template (can be overwritten).
        '''

        super(TAddHandler, self).__init__(page_template)
        self.save_path = os.getcwd()
        self.file_exists_template = '''
        <html><head>
        <title>File exists</title>
        </head>
        <body>
            <h2>Failed to add torrent</h2>
            <p>File %%(fname) exists, cannot add torrent</p>
        </body></html>
        '''

    def set_save_path(self, path):
        '''Sets save path to path. Throws on errors.'''

        if not os.path.isdir(path):
            raise RuntimeError("TAddHandler: '%s' is not a path" % path)
        self.save_path = os.path.realpath(path)

    def set_file_exists_template(self, template):
        '''Sets file_exists_template to template.

        Template should have %%(fname)s and %%(torrent_url)
        to be output correctly.
        '''

        self.file_exists_template = template

    def process(self, body=None, browser=None):
        '''Processes requests, body and browser should not be None.

        Gets topic url from body's 'url' parameter.
        Gets output filename from body's 'fname' parameter. Of fname is empty,
        it tries to get outname from Content-Type of remote site answer.

        It removes all .torrent siffixes from given fname, and adds one
        by itself.
        It does not overwrite existing files and reports errors on attempt.
        '''

        url = self.get_post_parameter(body, 'url')
        name = self.get_post_parameter(body, 'fname')

        # TODO: torrent get error
        torrent = browser.get_torrent(url)

        if len(name):

            while name.endswith('.torrent'):
                name = name[:-len('.torrent')]

            name = name + '.torrent'
        else:
            name = self.get_torrent_name(torrent.getheader('Content-Type'))

        if not len(name):
            name = 'new.torrent'

        fullname = os.path.join(self.save_path, name)

        if os.path.exists(fullname):
            # HTTP 409 Conflict
            status = 409
            headers = {'Content-Type': 'text/html'}

            params = {
                'torrent_url': url,
                'fname': fullname
            }
            body = self.file_exists_template % params
            return status, headers, body

        # TODO: write error
        with open(fullname, 'wb') as f:
            f.write(torrent.read())

        status = 200
        headers = {'Content-Type': 'text/html'}
        body = self.page_template % {
            'torrent_url': url,
            'torrent_name': name
        }
        return status, headers, body


    @staticmethod
    def get_post_parameter(body, param):
        '''Gets 'param' parameter from body and unquotes it.'''

        return urllib.unquote_plus(body[param])

    @staticmethod
    def get_torrent_name(header):
        '''Tries to get torrent name from string header (eg. 'Content-Type').

        Returns an empty string if fails.
        '''

        start = header.find('name="')
        if start == -1:
            return ''

        start = start + len('name="')
        finish = header.find('"', start)
        if finish == -1:
            finish = len(header)
        name = header[start:finish]

        return name

