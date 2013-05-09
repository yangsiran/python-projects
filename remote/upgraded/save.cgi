#!/usr/bin/env python2

print 'Content-type: text/html\n'

from os.path import join, abspath
import cgi, sha, sys


def halt(message):
    print """
    <div>%s</div>
    <div><a href="index.cgi">Return to home page.</a></div>
  </body>
</html>
""" % message
    sys.exit()


BASE_DIR = abspath('data')

form = cgi.FieldStorage()

text = form.getvalue('text')
filename = form.getvalue('filename')
password = form.getvalue('password')

print """
<html>
  <head>
    <title>Saving...</title>
  </head>
  <body>
"""

if not (filename and text and password):
    halt('Invalid parameters.')

if sha.sha(password).hexdigest() != '8843d7f92416211de9ebb963ff4ce28125932878':
    halt('Invalid password.')

f = open(join(BASE_DIR, filename), 'w')
f.write(text)
f.close()

print """
    <div>The file has been saved.</div>
    <div><a href="index.cgi">Return to home page.</a></div>
"""
# if filename.lower().endswith('.md'):
print '    <pre>%s</pre>' % text
print """
  </body>
</html>
"""
