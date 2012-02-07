#!/usr/bin/env python
"""
Generate an ELF with fewer sections:

   ./split.py elf:b0100000:b0140000

will read elf and split out elf-new with only the
sections for b0100000 and b0140000 and with an entry
address of b0100000.
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
    def write(self, f) :
        f.write(self.e_ident) 
        return f.write(struct.pack('<HHIIIIIHHHHHH', self.e_type, \
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
                self.e_shstrndx))

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
    def write(self, f) :
        return f.write(struct.pack('<IIIIIIII',
            self.p_type,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_flags,
            self.p_align))

def pr(x, pref) :
    for n in dir(x) :
        if pref == n[:len(pref)] :
            print '%s: %r' % (n, getattr(x, n))

def proc(fn, addrs) :
    if len(addrs) == 0 :
        raise Exception("no sections requested!")

    b = Buf(file(fn, 'rb').read())
    hdr = EHdr(b)

    # limitations of our quick hack
    if hdr.e_shnum != 0 or hdr.e_phoff != hdr.e_ehsize :
        raise Exception("unexpected format")

    #pr(hdr, 'e_')

    # load in program section headers and filter
    b.seek(hdr.e_phoff)
    phdrs = [PHdr(b) for n in xrange(hdr.e_phnum)]
    phdrs = [p for p in phdrs if p.p_vaddr in addrs]
    if len(phdrs) != len(addrs) :
        print 'want:', ['%x' % x for x in addrs]
        print 'got:', ['%x' % x.p_vaddr for x in phdrs]
        raise Exception("could not find all sections!")

    # load sections we want to keep
    for p in phdrs :
        b.seek(p.p_offset)
        p.data = b.read(p.p_filesz)

    # reuse same header with minor patches, and write out header and
    # program sections.
    f = file(fn + '-new', 'wb')
    hdr.e_phnum = len(phdrs)
    hdr.e_entry = addrs[0]
    hdr.write(f)
    for p in phdrs :
        p.write(f)
    f.close()
    

for arg in sys.argv[1:] :
    a = arg.split(':')
    fn,addrs = a[0],a[1:]
    addrs = [int(a, 16) for a in addrs]
    proc(fn, addrs)

