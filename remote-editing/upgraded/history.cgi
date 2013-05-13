#!/usr/bin/env python2

print 'Content-type: text/html\n'

import cgi
import sys
from MySQLdb import connect

form = cgi.FieldStorage()

filename = form.getvalue('filename')

if not filename:
    print 'Invalid paraters.'
    sys.exit()

db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor()

if not cur.execute("select date, user from files where name='%s'"
                   'order by date desc' % filename):
    print 'File does not exist.'
    sys.exit()

format = 'Markdown' if filename.lower().endswith('.md') else 'Plain text'
print '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>History - Remote Editing</title>
  </head>
  <body>
    <div>
      Filename: <em>%s</em> Format: <em>%s</em>
    </div>
    <table>
      <tr>
        <th>Modification</th>
        <th>Mender</th>
      </tr>
''' % (filename, format)

for date, user in cur.fetchall():
    print '''
      <tr>
        <td>%s</td>
        <td>%s</td>
        <td>
          <a href="view.cgi?filename=%s&date=%s"><small>View</small></a>
        </td>
      </tr>
''' % (date, user, filename, date)

print '''
    </table>
    <div>
      <a href="index.cgi">Return to home page.</a>
    </div>
  </body>
</html>
'''

db.close()
