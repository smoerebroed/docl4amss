#!/usr/bin/env python
"""
Sort the elf program headers by virtual address
and write it back out. 
This seems to fix an issue with skyeye failing
to see the bootinfo section.
"""

import sys, struct

def readfmt(f, fmt) :
    d = f.read(struct.calcsize(fmt))
    return struct.unpack(fmt, d)
def writefmt(f, fmt, *args) :
    f.write(struct.pack(fmt, *args))

class EHdr(object) :
    def __init__(self, f) :
        self.e_ident = f.read(16)
        (self.e_type,
                self.e_machine, 
                self.e_version, 
                self.e_entry, 
                self.e_phoff, 
                self.e_shoff, 
                self.e_flags, 
                self.e_ehsize, 
                self.e_phentsize, 
                self.e_phnum,
                self.e_shentsize,
                self.e_shnum,
                self.e_shstrndx) = readfmt(f, '<HHIIIIIHHHHHH')
    def write(self, f) :
        f.write(self.e_ident) 
        writefmt(f, '<HHIIIIIHHHHHH', self.e_type, 
                self.e_machine, 
                self.e_version, 
                self.e_entry, 
                self.e_phoff, 
                self.e_shoff, 
                self.e_flags, 
                self.e_ehsize, 
                self.e_phentsize, 
                self.e_phnum, 
                self.e_shentsize, 
                self.e_shnum, 
                self.e_shstrndx)

class PHdr(object) :
    def __init__(self, f) :
        (self.p_type,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_flags,
            self.p_align) = readfmt(f, "IIIIIIII")
    def write(self, f) :
        return writefmt(f, '<IIIIIIII',
            self.p_type,
            self.p_offset,
            self.p_vaddr,
            self.p_paddr,
            self.p_filesz,
            self.p_memsz,
            self.p_flags,
            self.p_align)

def pr(x, pref) :
    for n in dir(x) :
        if pref == n[:len(pref)] :
            print '%s=%r' % (n, getattr(x, n)),
    print
    

def proc(fn) :
    b = file(fn, 'rb+')
    hdr = EHdr(b)
    #pr(hdr, 'e_')

    # load in program section headers and filter
    b.seek(hdr.e_phoff)
    #print '%x' % hdr.e_phoff
    phdrs = [PHdr(b) for n in xrange(hdr.e_phnum)]
    phdrs.sort(key=lambda p : p.p_paddr)

    b.seek(hdr.e_phoff)
    for p in phdrs :
        p.write(b)
    for p in phdrs :
        print '%x - %x (%x) @ %x' % (p.p_paddr, p.p_paddr + p.p_memsz, p.p_paddr + p.p_filesz, p.p_vaddr)
    

for arg in sys.argv[1:] :
    proc(arg)

