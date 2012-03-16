"""
find all calls to logErr 
fix up the err structure passed in as arg0
and add comments to the code to make it more readable.

XXX add comments to uncommented functions with the
filename?
"""

def eachAddr(start, end) :
    while start < end :
        yield start
        start += 2

def getStr(x) :
    r = ''
    while 1 :
        c = Byte(x)
        x += 1
        if c < 0 or c > 0x7f :
            return
        if c == 0 :
            break
        r += chr(c)
    return r

def fixStr(start) :
    x = start
    while Byte(x) != 0 :
        x += 1
    MakeUnknown(start, x-start+1, DOUNK_SIMPLE)
    MakeStr(start, x+1)

def getFunc(addr) :
    return Name(addr), GetFunctionAttr(addr,FUNCATTR_START), GetFunctionAttr(addr, FUNCATTR_END)

def fixStruct(addr, sz, sname) :
    MakeUnknown(addr, sz, DOUNK_SIMPLE)
    MakeStruct(addr, sname)

def procLogErr(func, addr, info) :
    ws = [Dword(info + x) for x in 0,4,8,12,16]
    if any(x == 0xffffffff for x in ws) :
        print func, 'error, bad struct ptr or format'
        return
    msg,fname = getStr(ws[2]), getStr(ws[3])
    if msg is None or fname is None :
        print func, 'error, bad struct strings'
        return

    #print 'found err at %s %x: %s msg %s' % (func, addr, fname, msg)
    fixStruct(info, 5*4, 'errInfo')
    MakeRptCmt(info, '%s\n%s' % (fname, msg))
    return fname


def labelFunc(faddr) :
    nm,start,end = getFunc(faddr)
    if start == -1 :
        print "not in a function!"
        return 
    if not nm :
        nm = 'sub_%x' % start

    r0 = 0xffffffff
    fn = None
    for addr in eachAddr(start, end) :
        mn = GetMnem(addr)
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R0' :
            ld = addr
            r0 = Dword(GetOperandValue(addr, 1))
        if mn == 'ADR' and GetOpnd(addr, 0) == 'R0' :
            ld = addr
            r0 = GetOperandValue(addr, 1)
        if mn == 'BLX' or mn == 'BL' :
            op0 = GetOpnd(addr, 0)
            if 'logErr' in op0 :
                n = procLogErr(nm, addr, r0)
                fn = fn or n
                MakeComm(ld, '') # erase any obfuscating comment at the load site
            r0 = 0xffffffff

    if fn :
        print nm, "found", fn
        if not GetFunctionCmt(start, 0) and not GetFunctionCmt(start, 1) :
            SetFunctionCmt(start, fn, 1)
        else :
            print "not commenting on", nm
    
def funcs() :
    addr = NextFunction(0)
    while addr != BADADDR :
        yield addr
        addr = NextFunction(addr)

def labelAll() :
    for f in funcs() :
        labelFunc(f)

#labelFunc(ScreenEA())
labelAll()

