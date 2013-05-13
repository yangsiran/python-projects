#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgi
import sys
from sha import sha
from MySQLdb import connect
from markdown import markdown

form = cgi.FieldStorage()

filename = form.getvalue('filename')
user = form.getvalue('user')
password = form.getvalue('password')
content = form.getvalue('content')

if not (filename and user and password):
    print 'Invalid parameters.'
    sys.exit()

# The password is 'foobar'.
if sha(password).hexdigest() != '8843d7f92416211de9ebb963ff4ce28125932878':
    print 'Invalid password.'
    sys.exit()

db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()
cur.execute("update files set lastest = 0 where name='%s'" % filename)
cur.execute("insert into files (name, user, content) values ('%s', '%s', '%s')"
                                                   % (filename, user, content))
db.commit()

cur.execute("select date from files where name='%s' and lastest" % filename)
date = cur.fetchall()[0][0]
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
    <title>Saving - Remote Editing</title>
    <link type="text/css" rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div>The file has been saved.</div>
    <div>
      Filename: <em>%s</em> Format: <em>%s</em><br />
      Last edit by <em>%s</em> At <em>%s</em>
    </div>
    <div class="textbox">%s</div>
    <div>
      <a href="index.cgi">Return to home page.</a>
    </div>
  </body>
</html>
''' % (filename, format, user, date, content)
