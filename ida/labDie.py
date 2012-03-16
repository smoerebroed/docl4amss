"""
label a function with its filename
after finding it in a j__die2 argument

Looks only at function at current address..
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

def labelCurrent() :
    addr = ScreenEA()
    nm,start,end = getFunc(addr)
    if start == -1 :
        print "not in a function!"
        return 

    r1 = None
    fn = None
    for addr in eachAddr(start, end) :
        mn = GetMnem(addr)
        if mn == 'LDR' and GetOpnd(addr, 0) == 'R1' :
            r1 = Dword(GetOperandValue(addr, 1))
            print 'r1 %x' % r1
        if mn == 'ADR' and GetOpnd(addr, 0) == 'R1' :
            r1 = GetOperandValue(addr, 1)
        if mn == 'BLX' or mn == 'BL' :
            op0 = GetOpnd(addr, 0)
            if 'die' in op0 or 'reportErr' in op0 :
                if r1 is None or getStr(r1) is None :
                    print 'error, didnt get fname!'
                else :
                    fn = getStr(r1)
                break
                
            r1 = None

    if fn is None :
        print "not found!"
    else :
        print "found", fn
        fixStr(r1)
        SetFunctionCmt(start, fn, 1)
    

labelCurrent()

