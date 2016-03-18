import socket
import sys
import time
import random
import math
import csv
from random import gauss

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 49500)
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

notused1 = 0
notused2 = 0
currentSpeed = 0
currentLimit = 0
nextLimit = 0
distance = 0
gaspedal = 0.0
brakepedal = 0.0
msgTime = 0
lastTime = 0

SPEED_UP_FACTOR = 3
CSV_HEADER_LINES = 2

try:
    # with open('testdrive1.csv', 'rb') as csvfile:
    with open('testdrive2_popsUpToEarly.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')

        line = 0
        lastTime = 0
        for row in reader:
            if line >= 2 and len(row) is not 0:
                currentSpeed = row[0]
                currentLimit = row[1]
                nextLimit = row[2]
                distance = row[3]
                gaspedal = row[4]
                brakepedal = row[5]
                msgTime = row[6]
                reply = str(currentSpeed) + ';' + str(
                    currentLimit) + ';' + str(nextLimit) + ';' + str(distance) + ';' + str(
                    gaspedal) + ';' + str(brakepedal) + ';' + str(msgTime) + ';' + '\n'
                print 'Sending timestamp: ' + str(msgTime) + "  next sign in " + str(
                    int(float(distance))) + "m"

                sock.send(reply)
                time.sleep((float(msgTime) - float(lastTime)) / SPEED_UP_FACTOR)
                lastTime = msgTime
            line += 1





finally:
    print >> sys.stderr, 'closing sockets'
    sock.close()
