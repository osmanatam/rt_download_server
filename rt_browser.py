#!/usr/bin/env python


'''Module rt_broswer presents RutrackerBrowser.

    It allows getting .torrent files from RuTracker.Org.'''

import httplib
import re
import urllib
import urlparse


class RutrackerBrowserError(RuntimeError):
    '''RutrackerBrowserError raise on runtime errors.'''

    pass

class RutrackerBrowser(object):
    '''Class RutrackerBrowser presents browser for RuTracker.Org.

    It allows logging in and getting .torrent files from RuTracker.Org.'''
    _topic_re = re.compile('[\s/?&]t=(\d+)')

    def __init__(self, login, password):
        '''Initialises browser, stores RuTracker.Org's login and password.

        login    - RuTracker.org login;
        password - RuTracker.org password.'''

        self._login = login
        self._password = password
        self._cookie_auth = None


    def login(self):
        '''Logs in RuTracker.Org.

        This method should be called before any attempts to get .torrent files.'''

        data = {
            'login_username': self._login,
            'login_password': self._password
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0',
            'Referer': 'http://rutracker.org/forum/index.php',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = urllib.urlencode(data) + '&login=%C2%F5%EE%E4'

        conn = httplib.HTTPConnection('login.rutracker.org')
        #conn.set_debuglevel(2)
        conn.request('POST', '/forum/login.php', body=body, headers=headers)
        resp = conn.getresponse()
        conn.close()
        if resp.status != 302 and not resp.getheader('Set-Cookie', None):
            raise RutrackerBrowserError('could not login: %s' % resp.read())

        self._cookie_auth = self._get_auth_cookie(resp, 'bb_data')


    @staticmethod
    def check_topic_url(topic_url):
        '''Raises if topic_url is not valid.'''

        match = RutrackerBrowser._topic_re.search(topic_url)
        if not match:
            mess = "'%s' is not a valid topic url" % topic_url
            raise RutrackerBrowserError(mess)

    def open_topic_url(self, topic_url):
        '''Returns filelike object on succesfull topic getting.

        topic_url - url with viewtopic.php?t=3656915.'''

        self.check_topic_url(topic_url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0',
            'Referer': 'http://rutracker.org/forum/index.php',
            'Cookie' : self._cookie_auth

        }
        parsed_url = urlparse.urlparse(topic_url)

        conn = httplib.HTTPConnection('rutracker.org')
        #conn.set_debuglevel(2)
        path = '?'.join((parsed_url.path, parsed_url.query))
        conn.request('GET', path, headers=headers)

        res = conn.getresponse()
        conn.close()

        if res.status != 200:
            mess = "Could not open url \'%s\': status %d" % (topic_url, res.status)
            raise RutrackerBrowserError(mess)

        return res

    def get_torrent(self, topic_url):
        '''Returns filelike object with .torrent as its contents.

        topic_url - url with viewtopic.php?t=3656915.
        Use this method only for logined browser.'''

        self.check_topic_url(topic_url)

        res = self.open_topic_url(topic_url)
        # I need to get smth from auth cookie,
        # combine this parts + bb_dl=%(topic_id)s

        match = RutrackerBrowser._topic_re.search(topic_url)
        topic_id = match.group(1)

        cookie_dl = '%s; bb_dl=%s' % (self._cookie_auth, topic_id)

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0',
            'Referer': topic_url,
            'Cookie': cookie_dl
        }

        conn = httplib.HTTPConnection('dl.rutracker.org')
        #conn.set_debuglevel(2)
        conn.request('GET', '/forum/dl.php?t=%s' % topic_id, headers=headers)

        res = conn.getresponse()
        #conn.close()

        if res.status == 302:
            mess = "Could not get torrent from \'%s\': status 302: %s" % (topic_url, res.getheader('Location'))
            raise RutrackerBrowserError(mess)
        elif res.status != 200:
            mess = "Could not get torrent from \'%s\': status %d" % (topic_url, res.status)
            raise RutrackerBrowserError(mess)

        return res

    @staticmethod
    def _get_auth_cookie(resp, name):
        '''Returns cookie in format name=value from response.

        resp - response after HTTPConnection made request;
        name - name of a cookie to extract.'''

        cookie = resp.getheader('Set-Cookie')
        start = cookie.find(name)
        if start == -1:
            raise RutrackerBrowserError("no '%s' cookie. login failed" % name)
        finish = cookie.find(';', start)
        if (finish == -1):
            finish = len(cookie)

        return cookie[start:finish]

#expample
#    b = RutrackerBrowser()
#    res = b.get_torrent('http://rutracker.org/forum/viewtopic.php?t=3656915')
#    with open('test.torrent', 'wb') as f:
#        f.write(res.read())



