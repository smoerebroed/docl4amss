#!/usr/bin/env python
"""
Show memory at address from one of our memory dumps...
"""

import os, sys

def hexdump(addr, d) :
    def getChar(n) :
        if n >= 0 and n < len(d) :
            ch = d[n]
            if ch >= ' ' and ch <= '~' :
                return ch
            return '.'
        return ' '
    def getHex(n) :
        if n >= 0 and n < len(d) :
            return '%02x' % ord(d[n])
        return '  '
    o = -(addr & 15)
    while o < len(d) :
        h1 = ' '.join(getHex(o+n) for n in xrange(8))
        h2 = ' '.join(getHex(o+n+8) for n in xrange(8))
        cs = ''.join(getChar(o+n) for n in xrange(16))
        print '%08x: %-15s  %-15s | %s' % (addr+o, h1, h2, cs)
        o += 16

def findFile(addr) :
    for fn in os.listdir('.') :
        if '.bin' in fn :
            ws = fn.replace('.bin','').split('-')
            if ws[0] == 'mem' :
                x = int(ws[1], 16)
                sz = os.stat(fn).st_size
                if addr >= x and addr < x + sz :
                    return fn, addr - x
    raise Exception("Address not found: %x" % addr)

def dump(addr, n) :
    fn, off = findFile(addr)
    f = file(fn, 'rb')
    f.seek(off)
    d = f.read(n)
    print 'dumping %d at %x from %s' % (n, off, fn)
    hexdump(addr, d)

def num(x) :
    if x[:2] == '0x' :
        return int(x, 16)
    return int(x)

def main() :
    addr = num(sys.argv[1])
    n = num(sys.argv[2])
    dump(addr, n)

if __name__ == '__main__' :
    main()
