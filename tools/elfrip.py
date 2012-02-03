#!/usr/bin/env python
"""
Rip apart an elf into separate files for each program section.
Assumes little endian 32-bit elf file, with no error checking.
"""

import sys, struct

class Buf(object) :
    def __init__(self, dat) :
        self.pos = 0
        self.dat = dat
    def read(self, n) :
        x = self.dat[self.pos : self.pos + n]
        self.pos += n
        return x
    def seek(self, pos) :
        self.pos = pos
    def readUnpack(self, fmt) :
        sz = struct.calcsize(fmt)
        return struct.unpack("<" + fmt, self.read(sz))

class EHdr(object) :
    def __init__(self, b) :
        self.e_ident = b.read(16)
        self.e_type, \
                self.e_machine, \
                self.e_version, \
                self.e_entry, \
                self.e_phoff, \
                self.e_shoff, \
                self.e_flags, \
                self.e_ehsize, \
                self.e_phentsize, \
                self.e_phnum, \
                self.e_shentsize, \
                self.e_shnum, \
                self.e_shstrndx = b.readUnpack('HHIIIIIHHHHHH')

class PHdr(object) :
    def __init__(self, b) :
        (self.p_type,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_flags,
            self.p_align) = b.readUnpack("IIIIIIII")

def proc(fn) :
    b = Buf(file(fn, 'rb').read())
    hdr = EHdr(b)
    #print hdr.e_phnum, hdr.e_phentsize, hdr.e_phoff

    b.seek(hdr.e_phoff)
    phdrs = [PHdr(b) for n in xrange(hdr.e_phnum)]

    for p in phdrs :
        #print p.p_type, p.p_offset, p.p_filesz
        b.seek(p.p_offset)
        d = b.read(p.p_filesz)
        fn2 = '%s-%x' % (fn, p.p_offset)
        file(fn2, 'wb').write(d)

for fn in sys.argv[1:] :
    proc(fn)

