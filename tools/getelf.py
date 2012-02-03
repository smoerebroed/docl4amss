#!/usr/bin/env python
"""
Extract an ELF from a radio image by finding the first
ELF header in the file and then extracting everything until
the next blank section.
This is somewhat hokey but its easy and it works.
"""

import sys

gidx = 0

def getelf(fn) :
    global gidx
    gidx += 1
    d = file(fn, 'rb').read()
    idx1 = d.index('\x7fELF')
    idx2 = d.index('\xff' * 256, idx1)
    d = d[idx1 : idx2]
    file('elf-%d' % (gidx), 'wb').write(d)

for fn in sys.argv[1:] :
    getelf(fn)



