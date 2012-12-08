#!/usr/bin/env python

'''Module of base handlers for torent download server.

It declares two classes - IHandler which is the interface for all handlers.
TAnyHandler - handler of any request, which just prints given template.
'''

import abc

class IHandler(object):
    '''Interface for all handler classes.'''

    __mataclass__ = abc.ABCMeta

    def __init__(self, page_template):
        '''Saves page_template for succesfull reports.'''

        self.page_template = page_template

    @abc.abstractmethod
    def process(self, body=None, browser=None):
        '''Processes http request, returns (status, headers, body) on success.

        body - request body parameters;
        browser - RuTrackerBrowser instanse for getting torrents.

        Returns (status, None, None) on error (should be used with send_error).
        Can be (status, headers, None) for 3xx codes.
        '''

        return

class TAnyHandler(IHandler):
    '''Class for processing 'any' request, just returns page_template.

    In handlers mapping should be a value for the '*' key.
    '''

    def process(self, body=None, browser=None):
        '''Just returns own page_template.'''

        status = 200
        headers = {'Content-Type': 'text/html'}
        body = self.page_template

        return status, headers, body

