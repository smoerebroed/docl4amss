"""
find calls to __assert in ARM code and rename
functions according to the filename reported by assert.

Renames with a leading underscore to denote an auto rename that
might be incorrect (ie. due to inlining).
"""

def eachAddr(start, end) :
    while start < end :
        yield start
        start += 4

def findAssert(name, start, end) :
    r2 = None
    for addr in eachAddr(start, end) :
        mn = GetMnem(addr)
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R2' :
            r2 = GetOperandValue(addr, 1)
        if mn == 'BL' and GetOpnd(addr, 0) == '__assert' :
            return GetString(Dword(r2), -1, ASCSTR_C)

def procFunc(name, start, end) :
    if 0 or name[:4] == 'sub_' :
        nm2 = findAssert(name, start, end)
        if nm2 is not None :
            print 'Function: %s = %s' % (name, nm2)
            MakeNameEx(start, '_' + nm2, SN_CHECK | SN_AUTO)

def allFuncs() :
    addr = NextFunction(0)
    while addr != BADADDR :
        yield Name(addr), addr, GetFunctionAttr(addr, FUNCATTR_END)
        addr = NextFunction(addr)

def main() :
    for name,start,end in allFuncs() :
        procFunc(name, start, end)

main()

