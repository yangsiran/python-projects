import sys
import os

import markup


handler = markup.HTMLRenderer()
parser = markup.BasicTextParser(handler)

root = sys.argv[1]
for (dirpath, dirnames, filenames) in os.walk(root):
    for filename in filenames:
        if filename.endswith('.txt'):
            path = os.path.join(dirpath, filename)
            with open(path) as file:
                sys.stdout = open(path[:-3]+'html', 'w')
                parser.parse(file)
