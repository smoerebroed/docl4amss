"""
convert a region to strings...
"""

def fixDwords(start, end) :
    MakeUnknown(start, end - start, DOUNK_SIMPLE)
    e = start
    while e < end :
        MakeDword(e)
        e += 4

def fixOne(start, end) :
    MakeUnknown(start, end-start+1, DOUNK_SIMPLE)
    MakeStr(start, end+1)

def stringFix(start, end) :
    e = start
    while e < end :
        s = e
        while Byte(e) != 0 :
            e += 1
        fixOne(s, e)
        while Byte(e) == 0 :
            e += 1

def main() :
    #stringFix(0x17101928, 0x17130C1F)
    #stringFix(0x175418b8, 0x1756d644)
    #stringFix(0x17332424, 0x1734F7F4)
    #stringFix(0x1721AFAC, 0x1724057C)
    #stringFix(0x17653BA4, 0x1767CF54)

    #fixDwords(0x1767C44C, 0x1767C860)
    #fixDwords(0x1767C8AC, 0x1767C974)

    #stringFix(0x16F123EC, 0x16F125B4)
    #stringFix(0x16EF1648, 0x16F10840)

    #stringFix(0x171FA994, 0x171fabd0)

main()

