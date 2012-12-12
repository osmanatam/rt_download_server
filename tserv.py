#!/usr/bin/env python

'''Module presents TorrentServHandler class to use with BaseHTTPServer.'''

from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseRequestHandler

import Cookie

import auth
import page_template


class TorrentServHandler(BaseRequestHandler):
    '''Handler class for BaseHTTPServer to use with.

    It has own inner authorisation mechanism and output mechanism.
    '''

    server_version = 'TorrentDownloader/0.0'
    sys_version = ''

    def __init__(self, handlers, browser, *args, **kwargs):
        '''Initialises handler for use with BaseHTTPRequestHandler

        handlers - mapping of paths to handler objects;
        browser - browser for downloading .torrent files from topic urls.

        There should be '*' handler in handlers dict.
        There should be page_template.auth_path in handlers dict for authetification.

        On request server checks if user if authorized (via cookie).
        If not - it draws authorisation page from page_template.authorize, or
        processes authorisation via page_template.auth_handler path.
        If the user is authorized server checks path and calls
        corresponding handler's process method. If no such path->handler
        mapping - then it calls '*' handler.

        Cause this class needs to initialise parent's class, please wrap it
        with functools like:
            functools.partial(tserv.TorrentServHandler, handlers, browser)
        '''

        self.handlers = handlers
        self.browser = browser
        self.body = None
        BaseRequestHandler.__init__(
                self, *args, **kwargs
        )


    def do_GET(self):
        '''Processes GET method - it will be autorization or add page.'''

        if not self.is_authorized():
            self.authorization_page()
        else:
            self.body = None
            self.process('*')


    def do_POST(self):
        '''Processes POST methodn.

        If user is not authorized, only page_template.auth_path path, otherwise
        it calls handler for path (or handler for '*' if no such path.
        '''

        if not self.is_authorized() and self.path != page_template.auth_path:
            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.process_POST_body()
            self.process(self.path)



    def process(self, path):
        '''Call to handler of path of to handler of '*'.'''

        path = path.lstrip('/')
        if path not in self.handlers:
            path = '*'

        (status, headers, body) = self.handlers[path].process(self.body, self.browser)

        if not headers and not body:
            self.send_error(status)
            return

        self.send_response(status)

        for head, val in headers.iteritems():
            self.send_header(head, val)

        self.end_headers()

        if body:
            self.wfile.write(body)


    def extract_cookie_id(self):
        '''Extracts cookie from request, needed for authorisation check.'''

        c = Cookie.SimpleCookie(self.headers['cookie'])
        return c['ID'].value

    def is_authorized(self):
        '''Returns True if user is authorized, False otherwise.'''

        try:
            return 'cookie' in self.headers and auth.is_good_cookie(self.extract_cookie_id())
        except KeyError:
            return False

    def authorization_page(self):
        '''Draws autorisation page.'''

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        self.wfile.write(page_template.authorize)



    def process_POST_body(self):
        '''Extracts useful fields and setups state after POST request.'''

        contlength = int(self.headers['content-length'])
        s = self.rfile.read(contlength)
        self.body = dict(r.split('=') for r in s.split('&'))

