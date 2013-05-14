#!/usr/bin/env python2

print 'Content-type: text/html\n'

from MySQLdb import connect

db = connect(user='root', db='webapp',
             unix_socket='/opt/lampp/var/mysql/mysql.sock')
cur = db.cursor();

print '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Files - Remote Editing</title>
  </head>
  <body>
    <h1>Files</h1>
    <table>
      <tr>
        <th>File Name</th>
        <th>Last Modification</th>
      </tr>
'''

cur.execute('select name, date from files where lastest')
for (filename, date) in cur.fetchall():
    print '''
      <tr>
        <td><a href="view.cgi?filename=%s&date=%s">%s</a></td>
        <td>%s</td>
        <td>
          <a href="history.cgi?filename=%s"><small>Version Control</small></a>
        </td>
      </tr>
''' % (filename, date, filename, date, filename)

print '''
    </table>
    <form action="edit.cgi" method="POST">
      <strong>New File:</strong> <input type="text" name="filename" />
      <input type="submit" value="Create" />
    </form>
  </body>
</html>
'''

db.close()
