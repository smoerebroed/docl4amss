"""
quick hack to name task structures
in one particular function (startsmanythreads)
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

def fixStruct(addr, sz, sname) :
    MakeUnknown(addr, sz, DOUNK_SIMPLE)
    MakeStruct(addr, sname)

def getFunc(addr) :
    return Name(addr), GetFunctionAttr(addr,FUNCATTR_START), GetFunctionAttr(addr, FUNCATTR_END)

def fixStruct(addr, sz, sname) :
    MakeUnknown(addr, sz, DOUNK_SIMPLE)
    MakeStruct(addr, sname)

def procThread(addr, tname) :
    print 'name %x %s' % (addr, tname)
    MakeName(addr, 'task_' + tname)
    fixStruct(addr, 0x208, 'tcb') 


def labelFunc(faddr) :
    nm,start,end = getFunc(faddr)
    if start == -1 :
        print "not in a function!"
        return 
    if not nm :
        nm = 'sub_%x' % start

    r0 = 0xffffffff
    for addr in eachAddr(start, end) :
        mn = GetMnem(addr)
        if mn == 'LDR' :
            x = GetOpnd(addr, 1)
            if '=(thread' in x and '+1)' in x :
                tname = x[8:-3]
                #print 'found thread', tname
                
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R0' :
            ld = addr
            r0 = Dword(GetOperandValue(addr, 1))
        if mn == 'ADR' and GetOpnd(addr, 0) == 'R0' :
            ld = addr
            r0 = GetOperandValue(addr, 1)
        if mn == 'BLX' or mn == 'BL' :
            op0 = GetOpnd(addr, 0)
            if 'makeNewThread' in op0 :
                n = procThread(r0, tname)
            r0 = 0xffffffff
    
def funcs() :
    addr = NextFunction(0)
    while addr != BADADDR :
        yield addr
        addr = NextFunction(addr)

def labelAll() :
    for f in funcs() :
        labelFunc(f)

labelFunc(ScreenEA())
#labelAll()

