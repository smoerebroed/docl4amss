#!/usr/bin/env python
"""
Go into a radio image, extract the elf file, then
extract several programs from it as separate files.

  - elf: the entire elf file
  - ig_naming: just the sections for ig_naming
  - qdms: sections for qdms
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
    
def split(fn, outfn, *addrs) :
    if len(addrs) == 0 :
        raise Exception("no sections requested!")

    b = file(fn, 'rb')
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

    # patch header
    hdr.e_phnum = len(phdrs)
    hdr.e_entry = addrs[0]

    # load sections we want to keep, patching their offsets
    off = hdr.e_phoff + hdr.e_phentsize * hdr.e_phnum
    for p in phdrs :
        b.seek(p.p_offset)
        p.data = b.read(p.p_filesz)

        p.p_offset = off
        off += p.p_filesz

    # reuse same header with minor patches, and write out header and
    # program sections.
    print 'writing', outfn
    f = file(outfn, 'wb')
    hdr.write(f)
    for p in phdrs :
        #pr(p, 'p_')
        p.write(f)
    for p in phdrs :
        f.write(p.data)
    f.close()
    b.close()
    
def getelf(fn, outfn) :
    d = file(fn, 'rb').read()
    idx1 = d.index('\x7fELF')
    idx2 = d.index('\xff' * 256, idx1)
    print 'writing', outfn
    file(outfn, 'wb').write(d[idx1 : idx2])

def main(fn) :
    getelf(fn, 'elf')
    split('elf', 'ig_naming', 0xb0100000, 0xb0140000)
    split('elf', 'qdms', 0xb0200000, 0xb0240000)
    split('elf', 'quartz', 0xb0300000)
    split('elf', 'amss1', 0xb07000)
    split('elf', 'xxx1', 0xb0a000)
    split('elf', 'xxx2', 0x16e00000)
    

if __name__ == '__main__' :
    fn, = sys.argv[1:]
    main(fn)


