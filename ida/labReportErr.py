"""
label a function with its filename
after finding it in a reportErr argument
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

def labelFunc(faddr) :
    nm,start,end = getFunc(faddr)
    if start == -1 :
        print "not in a function!"
        return 
    if not nm :
        nm = 'sub_%x' % start

    r1 = 0xffffffff
    fn = None
    for addr in eachAddr(start, end) :
        mn = GetMnem(addr)
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R1' :
            r1 = Dword(GetOperandValue(addr, 1))
        if mn == 'ADR' and GetOpnd(addr, 0) == 'R1' :
            r1 = GetOperandValue(addr, 1)
        if mn == 'BLX' or mn == 'BL' :
            op0 = GetOpnd(addr, 0)
            if 'reportErr' in op0 :
                if r1 is None or getStr(r1) is None :
                    print 'error, didnt get fname!'
                else :
                    fn = getStr(r1)
                    fixStr(r1)
                
            r1 = 0xffffffff

    if fn :
        #print nm, "found", fn
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

