import socket, traceback 

host = ''                              # Bind to all interfaces 
port = 51000 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
s.bind((host, port))

bcast = ('<broadcast>', 20001)

s.sendto("\x0d\x00\x00\x00", bcast) 

while 1: 
    try: 
        message, address = s.recvfrom(8192) 
        print "Got data from", address 
        # Acknowledge it. 
        s.sendto("\x0d\x00\x00\x00", address) 
    except (KeyboardInterrupt, SystemExit): 
        raise 
    except: 
        traceback.print_exc() 