#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgi
import sys
from MySQLdb import connect

form = cgi.FieldStorage()

filename = form.getvalue('filename')
date = form.getvalue('date')

if not (filename):
    print 'Invalid paraters.'
    sys.exit()

if date:
    db = connect(user='root', db='webapp',
                 unix_socket='/opt/lampp/var/mysql/mysql.sock')
    cur = db.cursor()

    if not cur.execute('select user, content from files '
                       'where name=%s and date=%s', (filename, date)):
        print 'File does not exist'
        sys.exit()

format = 'Markdown' if filename.lower().endswith('.md') else 'Plain text'
print '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Editing - Remote Editing</title>
  </head>
  <body>
    <div>
      Filename: <em>%s</em> Format: <em>%s</em><br />
''' % (filename, format)

if date:
    user, content = cur.fetchall()[0]
    db.close()
    print '''
      Last edit by <em>%s</em> At <em>%s</em>
''' % (user, date)
else:
    content = ''

print '''
    </div>
    <form action="save.cgi" method="POST">
      <textarea name="content" cols=100 rows=40>%s</textarea><br />
      <b>User:</b> <input type="text" name="user" />
      <b>Password:</b> <input type="password" name="password" />
      <input type="hidden" name="filename" value="%s" />
      <input type="submit" value="Save" />
    </form>
    <div>
      <a href="index.cgi">Return to home page.</a>
    </div>
  </body>
</html>
''' % (content, filename)
