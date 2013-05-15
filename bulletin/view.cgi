#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgitb; cgitb.enable()

from MySQLdb import connect
db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()

import cgi, sys
form = cgi.FieldStorage()
id = form.getvalue('id')

try: id = int(id)
except:
    print 'Invalid message ID'
    sys.exit()

cur.execute('select * from messages where id=%s', id)
names = [d[0] for d in cur.description]
message = [dict(zip(names, row)) for row in cur.fetchall()]

try: message = message[0]
except IndexError:
    print 'Unknown message ID'
    sys.exit()


print """
<html>
  <head>
    <title>View Message</title>
  </head>
  <body>
    <h1>View Message</h1>
    <div>
      <strong>Subject:</strong> %(subject)s<br />
      <strong>Sender:</strong> %(sender)s<br />
    </div>
    <pre>%(text)s</pre>
    <hr />
    <div>
      <a href="main.cgi">Back to the main page.</a>
      |
      <a href="edit.cgi?reply_to=%(id)s">Reply</a>
    </div>
  </body>
</html>
""" % message
