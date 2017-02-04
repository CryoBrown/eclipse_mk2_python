import socket
import json

import time

import outputs

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--s', action="store", dest="server", help="ip address", default = "127.0.0.1")
parser.add_option('--c', action="store", dest="client", help="ip address", default = "127.0.0.1")
options, args = parser.parse_args()
print "SERVER IP:", options.server
print "CLIENT IP:", options.client

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address_me = (options.server, 5004)
address_u = (options.client, 5005)
serversocket.bind(address_me)

serversocket.settimeout(0.5)

#code for socket.SOCK_STREAM
#serversocket.listen(1) # become a server socket, maximum 1 connections
#connection, address = serversocket.accept()

# serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serversocket.bind(('10.117.77.164', 8089))
# serversocket.listen(1) # become a server socket, maximum 1 connections
# connection, address = serversocket.accept()

FILLPIN = 13
VENTPIN = 26
RELIEFENABLEPIN = 16
RELIEFPIN = 4 #20 when the wiring permits?
IGNITIONPIN = 18 #21 when the wiring permits?
HEATERENABLEPIN = 23

VALVE_FILL = outputs.BallValve(FILLPIN)
VALVE_VENT = outputs.BallValve(VENTPIN)

RELIEF_ENABLE = outputs.Enable(RELIEFENABLEPIN) #TODO: make a button
RELIEF_ENABLE.enable()

HEATER_ENABLE = outputs.Enable(HEATERENABLEPIN) #TODO: put this on

VALVE_RELIEF = outputs.ServoValve(RELIEFPIN)

#Ignition
OUTPUT_IGNITION = outputs.Ignition(IGNITIONPIN)

VALVE_TITLES = ('Fill', 'Relief', 'Vent')

DEFAULT_STATUSES = {'Fill':False, 'Relief':True, 'Vent':False, 'Ignition':False}

OUTPUTS = {'Fill':VALVE_FILL, 'Relief':VALVE_RELIEF, 'Vent':VALVE_VENT, 'Ignition':OUTPUT_IGNITION}

def update_outputs(stats):
	for valve in VALVE_TITLES:
		if stats[valve]:
			OUTPUTS[valve].open()
		else:
			OUTPUTS[valve].close()
	if stats["Ignition"]:
		OUTPUTS["Ignition"].start()

dic = {'load' : 0.0, 'pressure' : 0.0, 'thermo' : 0.0}
data = json.dumps(dic)

i = 0
while True:
        print "----------------------------------------------"
        print "BEGIN LOOP " + str(i)
        #print "\n"

        # dic = {'load' : 0.0, 'pressure' : 0.0, 'thermo' : 0.0}
        # data = json.dumps(dic)

        #print "DATA:"
        #print data
        print "SENDING..."
        try:
            serversocket.sendto(data, address_u)
            #connection.send(data)
            print "done."
        except:
            print "failed."
        print "\n"

        print "RECEIVING..."
        try:
            received, addr = serversocket.recvfrom(1024)
            #received = connection.recv(1024)
            print "done."
            #print "RECEIVED:"
            #print received
            #print "\n"
            stats = json.loads(received)
            print "UPDATING OUTPUTS"
            update_outputs(stats)
            print "done."
        except:
            print "failed"
        #print"\n"

        print "Sleeping"
        time.sleep(0.1)

        print "END LOOP " + str(i)
        print "----------------------------------------------\n"
        i+=1

# while True:
#         dic = {'load' : 0.0, 'pressure' : 0.0, 'thermo' : 0.0}
#         data = json.dumps(dic)
#         print "DATA:\n"
#         print data
#         connection.send(data)
#         print "good"
#         received = connection.recv(1028)
#         print "RECEIVED:\n"
#         print received
#         stats = json.loads(received)
#         print "STATUS:\n"
#         print stats
#         update_outputs(stats)