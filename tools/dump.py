#!/usr/bin/env python
"""
Dump the KIP and the boot info from an elf file like elfweaver
but even if the ELF file has no section headers.

Must be run with weaver and elf (from OKL4) in your python path.
Tested against okl4_release_1.4.1.1/tools/pyelf
"""

#import debug
import array, struct, sys

import elf.core
import weaver.l4_kcp, weaver.ig_bootinfo

def decode(d, mag, ty) :
    idx = d.index(mag)
    a = array.array('b', d[idx:])
    s = elf.core.ElfSection(data=a)
    s.transform(ty)
    s.output()

for fn in sys.argv[1:] :
    d = file(fn, 'rb').read()

    # find kip and print
    decode(d, 'L4\xe6K', weaver.l4_kcp.KcpSection)

    # find bootinfo and print
    decode(d, '\x10\x00\x01\x00\x1d\x02\x60\x19', weaver.ig_bootinfo.IgBootInfoSection)

