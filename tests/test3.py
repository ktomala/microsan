import socket, sys 
dest = ('<broadcast>', 20001) 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
s.sendto("\x0d\x00\x00\x00", dest) 
print "Looking for replies; press Ctrl-C to stop." 
while 1: 
    (buf, address) = s.recvfrom(2048) 
    if not len(buf): 
        break 
    print "Received from %s: %s" % (address, buf)