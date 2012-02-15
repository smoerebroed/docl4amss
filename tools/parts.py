#!/usr/bin/python

import sys
import struct

# total size 0x14e0000

def dump(fn) :
    print "dump", fn
    f = file(fn, "rb")
    #hoff = 0x19020
    hoff = 0x20
    hoff = 0
    bsize = 0x1
    for tab in (0x00040830, 0x00044830, 0x00064830 ) :
    #for tab in 0x00040830, :
        print '%08x' % tab
        f.seek(tab) 
        s = 0
        for n in xrange(20) :
            d = f.read(28)
            name,meta = d[:16],d[16:]
            name = name.replace('\x00', '')
            # not sure on the flags, pretty sure on off and len
            off,len,flags = struct.unpack("III", meta)
            if off == 0xffffffff :
                break
            #off += 0xe
            print '%-16s %08x %08x %08x (%08x)' % (name, off*bsize+hoff, len*bsize, flags, s)
            s += len
        print


for fn in sys.argv[1:] :
    dump(fn)

