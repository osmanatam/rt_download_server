#!/usr/bin/env python


'''Module rt_broswer presents RutrackerBrowser.

    It allows getting .torrent files from RuTracker.Org.'''

import cookielib
import re
import urllib
import urllib2


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
        self._cookie_jar = cookielib.CookieJar()
        self._url_opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self._cookie_jar)
        )


    def login(self):
        '''Logs in RuTracker.Org.

        This method should be called before any attempts to get some
        .torrent files.'''

        data = {
            'login_username': self._login,
            'login_password': self._password,
            'login'         : '%C2%F5%EE%E4'
        }
        resp = self._url_opener.open(
            'http://login.rutracker.org/forum/login.php',
            data=urllib.urlencode(data)
        )

        if not resp:
            raise RutrackerBrowserError('could not login')
        if 'login.php' in resp.geturl():
            raise RutrackerBrowserError('could not login: %s\n\n%s' %
                    (resp.geturl(), resp.read()))


    @staticmethod
    def check_topic_url(topic_url):
        '''Raises exception if topic_url is not valid.'''

        match = RutrackerBrowser._topic_re.search(topic_url)
        if not match:
            mess = "'%s' is not a valid topic url" % topic_url
            raise RutrackerBrowserError(mess)


    def open_topic_url(self, topic_url):
        '''Returns filelike object on succesfull topic getting.

        topic_url - url with viewtopic.php?t=3656915.
        Not necessary method.'''

        self.check_topic_url(topic_url)

        req = urllib2.Request(topic_url)
        req.add_header('Referer', 'http://rutracker.org/forum/index.php')

        res = self._url_opener.open(req)

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

        dl_url = 'http://dl.rutracker.org/forum/dl.php?t=%s' % topic_id
        req = urllib2.Request(dl_url)
        req.add_header('Referer', topic_url)

        res = self._url_opener.open(req)

        return res


#example
#if __name__ == '__main__':
#    b = RutrackerBrowser('login', 'password')
#    b.login()
#    res = b.get_torrent('http://rutracker.org/forum/viewtopic.php?t=3656915')
#    with open('test.torrent', 'wb') as f:
#        f.write(res.read())



