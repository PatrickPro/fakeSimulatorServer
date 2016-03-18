'''
    Simple socket server using threads
'''

import socket
import sys
import time
from thread import *

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 49500  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string
    conn.send('42;51;0\n')

    currentSpeed = 82.0
    currentLimit = 80
    distance = 150
    nextLimit = 60
    gaspedal = 1.0
    brakepedal = 0.0
    sendInterval = 3.0

    # infinite loop so that function do not terminate and thread do not end.
    x = 0
    repeat = 1
    while x < repeat:

        # Receiving from client
        reply = str(currentSpeed) + ';' + str(currentLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(
            gaspedal) + ';' + str(brakepedal) + '\n'

        print 'Sending: ' + reply
        conn.sendall(reply)
        time.sleep(sendInterval)
        if distance > 0:
            currentSpeed -= 0.16
            distance -= 1;
        else:
            currentSpeed = 82.0
            distance = 150
        x += 1

    # came out of loop
    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

s.close()
