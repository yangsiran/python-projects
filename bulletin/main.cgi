#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgitb; cgitb.enable()

from MySQLdb import connect
db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()

cur.execute('select * from messages')
names = [d[0] for d in cur.description]
messages = [dict(zip(names, row)) for row in cur.fetchall()]


toplevel = []
children = {}

for message in messages:
    parent_id = message['reply_to']
    if parent_id is None:
        toplevel.append(message)
    else:
        children.setdefault(parent_id, []).append(message)


def format(message):
    print '<p><a href="view.cgi?id=%(id)i">%(subject)s</a></p>' % message
    try: kids = children[message['id']]
    except KeyError: pass
    else:
        print '<blockquote>'
        for kid in kids:
            format(kid)
        print '</blockquote>'


print """
<html>
  <head>
    <title>The Foobar Bulletin Board</title>
  </head>
  <body>
    <h1>The Foobar Bulletin Board</h1>
    <div>
"""

for message in toplevel:
    format(message)

print """
    </div>
    <hr />
    <div><a href="edit.cgi">Post message.</a></div>
  </body>
</html>
"""
