#!/usr/bin/env python
"""
post-process the output of names.py to generate a rough
filename map of the AMSS code.
"""

def lines() :
    for l in file('log.txt', 'r') :
        l = l.strip()
        x,dummy = l.split(' ', 1)
        addr = int(x, 16)
        dummy,x = l.split(': ', 1)
        fns = x.split(' ')
        yield addr, fns

def firstUniq() :
    lastFn = None
    seen = set()
    for addr,fns in lines() :
        if len(fns) == 1 :
            fn = fns[0]
            if fn != lastFn :
                if False : # XXX if fn in seen :
                    print 'oops, saw', fn, 'again'
                else :
                    lastFn = fn
                    seen.add(fn)
                    yield addr, fn

for addr, fn in firstUniq() :
    print '%08x: %s' % (addr, fn)

