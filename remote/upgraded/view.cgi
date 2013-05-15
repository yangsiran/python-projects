#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgi
import sys
from MySQLdb import connect
from markdown import markdown

form = cgi.FieldStorage()

filename = form.getvalue('filename')
date = form.getvalue('date')

if not (filename and date):
    print 'Invalid paraters.'
    sys.exit()

db = connect(user='root', db='webapp',
                     unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()

if not cur.execute('select user, content from files '
                   'where name=%s and date=%s', (filename, date)):
    print 'File does not exist'
    sys.exit()

user, content = cur.fetchall()[0]
if filename.lower().endswith('.md'):
    format = 'Markdown'
    content = markdown(content)
else:
    format = 'Plain text'
    content = '<pre>%s</pre>' % content

print '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Viewing - Remote Editing</title>
    <link type="text/css" rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div>
      Filename: <em>%s</em> Format: <em>%s</em><br />
      Last edit by <em>%s</em> At <em>%s</em>
    </div>
    <div class="textbox">%s</div>
    <form action="edit.cgi" method="POST">
      <input type="hidden" name="filename" value="%s" />
      <input type="hidden" name="date" value="%s" />
      <input type="submit" value="Edit It" />
    </form>
    <div>
      <a href="index.cgi">Return to home page.</a>
    </div>
  </body>
</html>
''' % (filename, format, user, date, content, filename, date)
