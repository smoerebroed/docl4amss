#!/usr/bin/env python
"""
use gdb protocol to act as jtag console to okl4

gdb proto implemention is quick and hackish

---
to run okl4 from "elf" file:
 $ qemu-system-arm -M versatileab -s -S -kernel elf -m 256 \
       -curses -monitor stdio 

then in another window run this program:
 $ ./cons-gdb.py


notes:
   http://davis.lbl.gov/Manuals/GDB/gdb_31.html
"""

import socket, sys

class Error(Exception) : pass

def pkt(d) :
    """gdb packet"""
    s = sum(ord(ch) for ch in d) & 0xff
    return '$%s#%02x' % (d, s)

def unrle(r) :
    while '*' in r :
        x = r.index('*')
        c = ord(r[x+1]) - 29
        r = r[:x] + r[x-1] * c + r[x+2:]
    return r

def unpkt(p) :
    if p[0] != '$' or p[-3] != '#' :
        raise Error('bad format')
    d = p[1:-3]
    s = sum(ord(ch) for ch in d) & 0xff
    if s != int(p[-2:], 16) :
        raise Error('bad cksum')
    return unrle(d)

def getPkt(s) :
    r = []
    while len(r) < 3 or r[-3] != '#' :
        ch = s.recv(1)
        if not ch :
            raise Error('eof')
        r.append(ch)
        if r[0] != '$' :
            raise Error('bad format')
    return unpkt(''.join(r))

def sendCmd(s, d) :
    s.send(pkt(d))
    ch = s.recv(1)
    if ch != '+' :
        raise Error("bad ack")
    return getPkt(s)

def cont(s, addr=None) :
    if addr :
        return sendCmd(s, 'c%x' % addr)
    return sendCmd(s, 'c')

def bpt(s, addr) :
    return sendCmd(s, "Z1,%x,4" % addr)

def unbpt(s, addr) :
    return sendCmd(s, "z1,%x,4" % addr)

def lehex(v) :
    return ''.join('%02x' % ((v >> n) & 0xff) for n in [0,8,16,24])

def unlehex(v) :
    if len(v) != 8 :
        raise Error('bad lehex: %r' % v)
    return int(v[0:2], 16) | (int(v[2:4], 16) << 8) | (int(v[4:6], 16) << 16) | (int(v[6:8], 16) << 24) 

def setRegs(s, vs) :
    vstr = ''.join(lehex(v) for v in vs)
    return sendCmd(s, 'G%s' % vstr)

def setReg(s, r, v) :
    vs = getRegs(s)
    vs[r] = v
    return setRegs(s, vs)

def splitn(s, n) :
    return [s[p : p + n] for p in xrange(0, len(s), n)]

def getRegs(s) :
    x = sendCmd(s, 'g');
    return [unlehex(v) for v in splitn(x, 8)]

def getReg(s, r) :
    return getRegs(s)[r]

def step(s) :
    return sendCmd(s, 's')

def detach(s) :
    s.send(pkt('D'))

def connect(port=1234) :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    return s

def stepBpt(s, addr) :
    unbpt(s, addr)
    step(s)
    bpt(s, addr)

def getCh() :
    """Get char in raw mode."""
    import tty, termios
    fd = sys.stdin.fileno()
    orig = termios.tcgetattr(fd)
    try :
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally :
        termios.tcsetattr(fd, termios.TCSADRAIN, orig)
    return ch

def runCons() :
    PC=15
    LR=14
    SP=13
    
    GETC = 0xf000f3f8
    PUTC = 0xf000f3bc
    
    s = connect()
    print bpt(s, GETC)
    print bpt(s, PUTC)
    
    while 1 :
        cont(s)
        reg = getRegs(s)
        if reg[PC] == PUTC :
            sys.stdout.write(chr(reg[0]))
            sys.stdout.flush()
        elif reg[PC] == GETC :
            ch = getCh()
            if ch in ['', '\x03', '\x04'] : # eof, ^c or ^d quits
                break
            reg[0] = ord(ch)
            reg[PC] = reg[LR]
            setRegs(s, reg)
            continue
    
        else :
            print 'done at %x' % reg[PC]
            break
        stepBpt(s, reg[PC])
    
    print 'done...'
    
    # XXX gdb somehow signals qemu to start down but I'm not sure
    # which packet does that..  for now we have to manuall stop qemu

try :
    runCons()
except Exception, e :
    print 'exception: %r' % e

