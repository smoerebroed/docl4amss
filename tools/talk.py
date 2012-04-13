#!/usr/bin/python
"""
talk to directly to the radio tty
Run "stop ril-daemon" first.

hints: 
  ATV1 - turn on verbose
  AT@BUILDDATE - show build info
"""

import fcntl, os, select, sys, termios, tty

def blocking(fd, flag) :
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    if flag :
        fl |= os.O_NONBLOCK
    else :
        fl &= os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, fl)

orig = {}

def rawOn(fd) :
    orig[fd] = termios.tcgetattr(fd)
    tty.setraw(fd)
    blocking(fd, 1)

def rawOff(fd) :
    termios.tcsetattr(fd, termios.TCSADRAIN, orig[fd])
    blocking(fd, 1)

echo = True

def copy(i, o, ctrl=False) :
    #print 'read from', i
    buf = os.read(i, 1)
    if buf == '' :
        return 'eof'
    if ctrl :
        if '\x04' in buf :
            return 'eof'
        if echo :
            os.write(i, buf)
        buf = buf.replace('\n', '\r')
    else :
        buf = buf.replace('\r', '\n')
    #print 'got %r' % buf
    os.write(o, buf)
    #print 'written'

def copier(x, y) :
    while 1 :
        r,w,e = select.select([x,y], [], [], None)
        if x in r and copy(x, y, 1) :
            print 'local closed'
            break
        if y in r and copy(y, x) :
            print 'remote closed' 
            break
    print 'done'

def main() :
    fd1 = sys.stdin.fileno()
    fd2 = os.open('/dev/smd0', os.O_RDWR)
    print fd1, fd2
    try :
        rawOn(fd1)
        rawOn(fd2)
        copier(fd1, fd2)
    finally :
        print 'cleanup'
        rawOff(fd1)
        rawOff(fd2)

if __name__ == '__main__' :
    main()

