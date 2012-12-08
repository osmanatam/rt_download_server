#!/usr/bin/env python

'''This is a template strings for torrent add server.'''

auth_path = '/auth'

header = '''<html><head><title>Torrent Add</title></head>\n
<body>'''

footer = '''<p><a href="/">Main Page</a></p>
</body></html>'''

index = '''%s
<form action="/torrentadd" method="post" name="torrents">
    Torrent URL:
    <input type="url" name="url">
    Filename:
    <input type="text" name="fname">.torrent
    <input type="submit" value="Add">
</form>
%s
''' % (header, footer)

success = '''%s
<h2>Success</h2>
<p>Torrent <a href="%%(torrent_url)s">%%(torrent_url)s</a> added succesfully as %%(torrent_name)s!</p>
%s
''' % (header, footer)

fail = '''%s
<h2>Fail</h2>
<p>Failed to add <a href="%%(torrent_url)s">%%(torrent_url)s</a> torrent!</p>
%s
''' % (header, footer)

file_exists = '''%s
<h2>Failed to add torrent</h2>
<p>File %%(fname)s exists, cannot add <a href="%%(torrent_url)s">%%(torrent_url)s</a> torrent!</p>
%s
''' % (header, footer)

authorize = '''%s
<h2>Identify yourself</h2>
<form action="%s" method="post">
    <p>Username: <input type="text" name="uname">
    Password: <input type="password" name="passwd">
    <input type="submit" value="Login">
</form>
%s
''' % (header, auth_path, footer)

