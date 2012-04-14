#!/usr/bin/python
"""
talk to radio tty and use AT commands to dump memory.
Run "stop ril-daemon" first.
"""

import os, sys

fd = os.open('/dev/smd0', os.O_RDWR)

def cmd(s) :
    os.write(fd, s + '\r')
    buf = ''
    while '\r\n0\r' not in buf :
        ch = os.read(fd, 1)
        if ch == '' :
            raise Exception('eof')
        buf += ch
    return buf[:-2]

def byte(x) :
    x = cmd('at@test=%d' % x).strip()
    for s in x.split('\n') :
        if s[:3] == '@: ' :
            return int(s[3:], 16)
    raise Exception('bad response: %r!' % x)

def num(x) :
    if x[:2].lower() == '0x' :
        return int(x[2:], 16)
    return int(x)
    
def dump(x, l) :
    for n in xrange(l) :
        print '%02x' % byte(x+n),
        sys.stdout.flush()
    print
    
def main() :
    if len(sys.argv) != 3 :
        raise Exception('usage: %s start len' % (sys.argv[0]))
    start = num(sys.argv[1])
    l = num(sys.argv[2])
    dump(start, l)

main() 
