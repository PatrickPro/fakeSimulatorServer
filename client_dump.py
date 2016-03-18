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
distance = 310
nextLimit = 60
gaspedal = 1.0
brakepedal = 0.0
sendInterval = 0.25

distanceSteps = 5

my_mean = 5
my_variance = 10


def accel(fromSpeed, toSpeed):
    global currentSpeed
    global distance
    global currentLimit
    global nextLimit
    global gaspedal
    global brakepedal
    global reply
    currentSpeed = fromSpeed
    print "accelerating"

    while currentSpeed < toSpeed:
        reply = str(currentSpeed) + ';' + str(currentLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(
                gaspedal) + ';' + str(brakepedal) + '\n'
        sock.send(reply)
        time.sleep(sendInterval / 2)
        currentSpeed += 1
        # distance -= distanceSteps;
    return


def keepSpeed(speed, holdTime):
    global currentSpeed
    global distance
    global currentLimit
    global nextLimit
    global gaspedal
    global brakepedal
    global reply
    currentSpeed = speed
    print "keeping speed"
    startTime = int(round(time.time() * 1000))

    while startTime + (holdTime * 1000) >= int(round(time.time() * 1000)):
        reply = str(currentSpeed) + ';' + str(currentLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(
                gaspedal) + ';' + str(brakepedal) + '\n'
        print 'Keeping speed: ' + reply
        sock.send(reply)
        time.sleep(sendInterval)

        rand = gauss(my_mean, math.sqrt(my_variance))
        # distance -= distanceSteps;
        if rand > 9:
            currentSpeed = speed + 1
        elif rand > 6:
            currentSpeed = speed
        else:
            currentSpeed = speed - 1
    return


try:
    time.sleep(2)
    # accel(0, 81)
    keepSpeed(80, 3)

    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        reply = str(currentSpeed) + ';' + str(currentLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(gaspedal) + ';' + str(brakepedal) + int(round(time.time() * 1000)) + '\n'

        print 'Sending: ' + reply
        sock.send(reply)
        time.sleep(sendInterval)
        if distance > 0 and currentSpeed > 0:
            rand = gauss(my_mean, math.sqrt(my_variance))
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
                drag = 0.4

            currentSpeed += (drag * magic)

            distance -= 2 * distanceSteps;
        # elif distance == 0:
        #
        #     reply = str(currentSpeed) + ';' + str(nextLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(
        #     gaspedal) + ';' + str(brakepedal) + '\n'
        #     sock.send(reply)
        #     time.sleep(5)
        #     distance = 310

        else:
            time.sleep(3.1)
            sock.send("dump")
            break
            time.sleep(6)
            # currentSpeed = 82.0
            distance = 310
            # accel(0, 81)
            keepSpeed(80, 6)





finally:
    print >> sys.stderr, 'closing sockets'
    sock.close()
