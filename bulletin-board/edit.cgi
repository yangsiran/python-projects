#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgitb; cgitb.enable()

from MySQLdb import connect
db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()

import cgi, sys
form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print """
<html>
  <head>
    <title>Compose Message</title>
  </head>
  <body>
    <h1>Compose Message</h1>

    <form action="save.cgi" method="POST">
"""

subject = ''
if reply_to is not None:
    print '      <input type="hidden" name="reply_to" value="%s" />' % reply_to
    cur.execute('select subject from messages where id = %s', reply_to)
    subject = cur.fetchone()[0]
    if not subject.startswith('Re: '):
        subject = 'Re: ' + subject

print """
      <strong>Subject:</strong><br />
      <input type="text" size="40" name="subject" value="%s" /><br />
      <strong>Sender:</strong><br />
      <input type="text" size="40" name="sender" /></br />
      <strong>Message:</strong><br />
      <textarea name="text" cols="40" rows="20"></textarea><br />
      <input type="submit" value="Save" />
    </form>
    <hr />
    <div><a href="main.cgi">Back to the main page.</a></div>
  </body>
</html>
""" % subject
