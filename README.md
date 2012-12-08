RuTracker.Org download server
==================

Server and browser for downloading .torrent files from RuTracker.Org.

What
------------------

This repo consists of a server which allows authorized users to download .torrent files from RuTracker.Org to specified folder. It asks for RuTracker.Org login/password on start, then starts listening on a specified port and attempting to download .torrent files. This allows you to add .torrent files to your .torrent downloader (if it tracks folder for new .torrent files to download) via http.

This repo also has a RuTrackerBrowser class which simplifies authorization and downloading .torrent files from RuTracker.org.

Requirements
------------------

Tested it with Python 2.7.3, but I think it should work with 2.6 too.

Usage
------------------

Server starts with main.py script, which takes parameters:
* -c, --config=file config - path to config file;
* -p, --port=port port - override config's port;
* -h, --help - print help message and exit.

Config
------------------

Looks like .ini config file, there is an example inside. Typical config should have [Server] section with 'port' and 'save_path' variables; and [Users] section with user-password pairs.
Server has its own authorization, so not everyone is allowed to add torrents to you machine, but it is easy crackable. You can change it in auth.py.

RuTrackerBrowser
------------------

It is a helper class to make authorization on RuTracker.Org easier. It can be found in rt_browser.py. It does not relogin automatically, so server will fail to add new torrents when authorization cookie will expire.

Extending
------------------

Handling requests is based on path - if you are not authorized, you can see authorization page or make attempt to authorize. Otherwise it looks for handler in path -> handler dictionary and call its process method. If no special handler for this path found, then handler for '*' is called


Prettifying
------------------

All html templates are in page_template.py page, but be careful with separate files like images or script files - ther is no handler that can get them - you will be shown just login or torrent add page. You have to write extension to have ability to include files.

