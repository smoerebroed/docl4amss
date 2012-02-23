"""
Matches unnamed functions against previously generated signatures.
"""

WILDCARD = 0x11111111
MINMATCH = 4

def eachAddr(start, end) :
    while start < end :
        yield start
        start += 4

def matches(sigs, ws) :
    for nm, xs in sigs.items() :
        if len(xs) == len(ws) and all(x == WILDCARD or x == w for (x,w) in zip(xs, ws)) :
            yield nm

def procFunc(sigs, name, start, end) :
    ws = [Dword(a) for a in eachAddr(start, end)]
    nms = list(matches(sigs, ws))
    if len(nms) == 1 :
        nm = nms[0]
        print "found %s = %s" % (name, nm)
        MakeNameEx(start, '_' + nm, SN_CHECK | SN_AUTO)
    if len(nms) > 1 :
        print "multiple matches for %s: %s" % (name, ','.join(nms))


def loadSigs(fn) :
    r = {}
    for l in file(fn) :
        ws = filter(None, l.strip().split(' '))
        name = ws[0]
        xs = [int(w, 16) for w in ws[1:]]
        if len([x for x in xs if x != WILDCARD]) >= MINMATCH :
            r[name] = xs
    return r

def allFuncs() :
    addr = NextFunction(0)
    while addr != BADADDR :
        yield Name(addr), addr, GetFunctionAttr(addr, FUNCATTR_END)
        addr = NextFunction(addr)

def main() :
    sigs = loadSigs('sigs.txt')
    for name,start,end in allFuncs() :
        if name[:4] == 'sub_' :
            procFunc(sigs, name, start, end)

main()

