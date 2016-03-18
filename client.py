import socket
import sys
import time
import random
import math
from random import gauss


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 49500)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

currentSpeed = 82.0
currentLimit = 80
distance = 280
nextLimit = 60
gaspedal = 1.0
brakepedal = 0.0
sendInterval = 0.25

my_mean = 5
my_variance = 10

try:
    time.sleep(2)

    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        reply = str(currentSpeed) + ';' + str(currentLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(
                gaspedal) + ';' + str(brakepedal) + int(round(time.time() * 1000)) +'\n'

        print 'Sending: ' + reply
        sock.send(reply)
        time.sleep(sendInterval)
        if distance > 0 and currentSpeed > 0:
            rand = gauss(my_mean, math.sqrt(my_variance))
            print 'rand: ' + str(rand)
            if rand > 8:
                # accel
                magic = 1
                gaspedal = 1.0
                brakepedal = 0.0
                drag = 0.5

            elif rand > 7:
                # brake
                magic = -1
                gaspedal = 0.0
                brakepedal = 1.0
                drag = 1
            else:
                # coast
                magic = -1
                gaspedal = 0.0
                brakepedal = 0.0
                drag = 0.5

            currentSpeed += (drag * magic)

            distance -= 5;
        else:
            time.sleep(2)
            currentSpeed = 82.0
            distance = 280





finally:
    print >> sys.stderr, 'closing sockets'
    sock.close()


