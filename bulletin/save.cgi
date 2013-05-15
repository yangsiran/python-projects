#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgitb; cgitb.enable()

from MySQLdb import connect
db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()

import cgi, sys
form = cgi.FieldStorage()

sender = form.getvalue('sender')
subject = form.getvalue('subject')
text = form.getvalue('text')
reply_to = form.getvalue('reply_to')

if not (sender and subject and text):
    print 'Please supply sender, subject, and text'
    sys.exit()

if reply_to is not None:
    cur.execute('insert into messages (reply_to, sender, subject, text) '
                'values (%s, %s, %s, %s)', (reply_to, sender, subject, text))
else:
    cur.execute('insert into messages (sender, subject, text) '
                'values (%s, %s, %s)', (sender, subject, text))

db.commit()

print """
<html>
  <head>
    <title>Message Saved</title>
  </head>
  <body>
    <h1>Message Saved</h1>
    <hr />
    <div><a href="main.cgi">Back to the main page.</a>
  </body>
</html>
"""
