#!/usr/bin/env python2

print 'Content-type: text/html\n'

import os

BASE_DIR = os.path.abspath('data')

print """
<html>
  <head>
    <title>File Editor</title>
  </head>
  <body>
    <h1>Files</h1>
    <div>
"""

for name in os.listdir(BASE_DIR):
  if os.path.isfile(os.path.join(BASE_DIR, name)):
      print """
      <a href="edit.cgi?filename=%s">%s</a>
      <small><a href="version.cgi?filename=%s">Version Control</a></small>
      <br />
""" % (name, name, name)

print """
</div>
    <form action="edit.cgi" method="POST">
      <b>New File:</b> <input type="text" name="filename" />
      <input type="submit" value="Create" />
    </form>
  </body>
</html>
"""
