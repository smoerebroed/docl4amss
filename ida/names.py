"""
find file names with logErr and reportErr and report them
"""

def eachAddr(start, end) :
    while start < end :
        yield start
        start += 2

def getStr(x) :
    if not x :
        return
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

def getFunc(addr) :
    return Name(addr), GetFunctionAttr(addr,FUNCATTR_START), GetFunctionAttr(addr, FUNCATTR_END)

def procLogErr(func, addr, info) :
    ws = [Dword(info + x) for x in 0,4,8,12,16]
    if any(x == 0xffffffff for x in ws) :
        print func, 'error, bad struct ptr or format'
        return
    msg,fname = getStr(ws[2]), getStr(ws[3])
    if msg is None or fname is None :
        print func, 'error, bad struct strings'
        return
    return fname

def labelFunc(faddr) :
    nm,start,end = getFunc(faddr)
    if start == -1 :
        print "not in a function!"
        return 
    if not nm :
        nm = 'sub_%x' % start

    r0 = 0xffffffff
    fn = set()
    for addr in eachAddr(start, end) :
        mn = GetMnem(addr)
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R0' :
            r0 = Dword(GetOperandValue(addr, 1))
        if mn == 'ADR' and GetOpnd(addr, 0) == 'R0' :
            r0 = GetOperandValue(addr, 1)
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R1' :
            r1 = Dword(GetOperandValue(addr, 1))
        if mn == 'ADR' and GetOpnd(addr, 0) == 'R1' :
            r1 = GetOperandValue(addr, 1)
        if mn == 'BLX' or mn == 'BL' :
            op0 = GetOpnd(addr, 0)
            if 'logErr' in op0 :
                n = procLogErr(nm, addr, r0)
                if n :
                    fn.add(n)
            if 'reportErr' in op0 :
                n = getStr(r1)
                if n :
                    fn.add(n)
                
            r0 = 0xffffffff
            r1 = 0xffffffff

    if fn :
        print '%08x %s found: %s' % (start, nm, ' '.join(list(fn)))
        print >>log, '%08x %s found: %s' % (start, nm, ' '.join(list(fn)))

def funcs() :
    addr = NextFunction(0)
    while addr != BADADDR :
        yield addr
        addr = NextFunction(addr)

def labelAll() :
    for f in funcs() :
        labelFunc(f)

log = file('log.txt', 'w')
#labelFunc(ScreenEA())
labelAll()
log.close()
