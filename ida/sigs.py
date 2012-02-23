"""
Generate signatures for each named function.
"""

WILDCARD = 0x11111111

def refsMem(addr) :
    memTypes = [2,3,4,6,7]
    return any(GetOpType(addr, n) in memTypes for n in xrange(3))

def eachAddr(start, end) :
    while start < end :
        yield start
        start += 4

def procFunc(f, name, start, end) :
    print "generating", name
    f.write(name + " ");
    for addr in eachAddr(start, end) :
        x = Dword(addr)
        if refsMem(addr) :
            x = WILDCARD
        f.write('%x ' % x)
    f.write('\n')

def allFuncs() :
    addr = NextFunction(0)
    while addr != BADADDR :
        yield Name(addr), addr, GetFunctionAttr(addr, FUNCATTR_END)
        addr = NextFunction(addr)

def main() :
    f = file('sigs.txt', 'w')
    for name,start,end in allFuncs() :
        if name[:4] != 'sub_' :
            procFunc(f, name, start, end)
    f.close()

main()

