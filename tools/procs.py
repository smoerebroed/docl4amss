#!/usr/bin/env python

import sys, struct

# for using dm interface....
"""
import dm
dm.quiet = 1
dm.initDev()

def getBuf(addr) :
        r = dm.peekb(4, addr)
        if r.code != 2 :
                raise Exception("read failed at %x!" % (addr))
    return r.data[:4]
"""

# for using AT@test interface
import mem
def getBuf(addr) :
    return ''.join(chr(mem.byte(addr+n)) for n in xrange(4))

class Proc(object) :
    def __init__(self, addr) :
        self.addr = addr
        # for gobi3k
        """ 
        self.name = self.getName(0x9c)
        self.id = self.getNum(0xd8)
        self.prev = self.getNum(0x40)
        self.next = self.getNum(0x44)
        self.stacklim = self.getNum(0xc)
        self.stack = self.getNum(0x10)
        self.stacksz = self.getNum(0xc0)
        self.utcb = self.getNum(0xb0)
        self.l4tid = self.getNum(0xa8)
        """
        # for adp1
        self.name = self.getName(0x70)
        self.id = self.getNum(0)
        self.prev = self.getNum(0x34)
        self.next = self.getNum(0x38)
        self.stacklim = self.getNum(0xc)
        self.stack = self.getNum(0x10)
        self.stacksz = self.getNum(0xc0)
        self.utcb = self.getNum(0xb0)
        self.l4tid = self.getNum(0x7c)

        #self.sp = self.getNumAbs(self.utcb + 0x54)
        #self.ip = self.getNumAbs(self.utcb + 0x58)

    def getNumAbs(self, addr) :
        return struct.unpack("<I", getBuf(addr)[:4])[0]
    def getNum(self, off) :
        return struct.unpack("<I", getBuf(self.addr + off)[:4])[0]
    def getName(self, off) :
            b = (getBuf(self.addr + off) +
                 getBuf(self.addr + off + 4) +
                 getBuf(self.addr + off + 8))
            return b.replace('\0', '')
    def peek4(self, x) :
        x -= self.addr
        if x >= 0 and x < 0x10000 :
            return self.getNum(x)
    def __str__(self) :
        return 'Task %r id:%x tcb:%x next:%x prev:%x stack:%x stacksz:%x stacklim:%x utcb:%x l4tid:%x' % (self.name, self.id, self.addr, self.next, self.prev, self.stack, self.stacksz, self.stacklim, self.utcb, self.l4tid)

def inCode(x) :
    return x >= 0x2f1000 and x < 0xb3d000

def stack(p) :
    sp = p.sp
    print 'stack:', #p.stacksz, (p.stacklim-sp),
    while sp < p.stacklim :
        x = p.peek4(sp)
        #print x,
        if inCode(x) :
            print hex(x),
        sp += 4
    print

def procs(addr=0x13a3758) :
    """
    print 'find first...'
    while 1 :
        p = Proc(addr)
        if not p.prev :
            break
        addr = p.prev
    print 'found...'
    """
    while addr :
        p = Proc(addr)
        yield p
        addr = p.next

def dump(start) :
    for p in procs(start) :
        print p
        #print '%x %x %s' % (p.getNum(0xe0), p.getNum(0xdc), p)
        if 0 :
            print p.name,
            stack(p)

if __name__ == '__main__' :
    #start = int(sys.argv[1], 16)
    #start = 0x13a3758      # gobi3k 2010
    start = 0x1a1bbb4       # adp1
    dump(start)

