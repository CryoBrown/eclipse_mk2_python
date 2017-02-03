import socket
import json

import outputs


FILLPIN = 19
RELIEFPIN = 16
VENTPIN = 26
IGNITIONPIN = 20

VALVE_FILL = outputs.BallValve(FILLPIN)
VALVE_VENT = outputs.BallValve(VENTPIN)

VALVE_RELIEF = outputs.ServoValve(RELIEFPIN)

#Ignition
OUTPUT_IGNITION = outputs.Ignition(IGNITIONPIN)

VALVE_TITLES = ('Fill', 'Relief', 'Vent')

DEFAULT_STATUSES = {'Fill':False, 'Relief':True, 'Vent':False, 'Ignition':False}

OUTPUTS = {'Fill':VALVE_FILL, 'Relief':VALVE_RELIEF, 'Vent':VALVE_VENT, 'Ignition':OUTPUT_IGNITION}

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind(('10.117.77.164', 8089))
serversocket.listen(1) # become a server socket, maximum 1 connections
connection, address = serversocket.accept()

def update_outputs(stats):
	for valve in VALVE_TITLES:
		if stats[valve]:
			OUTPUTS[valve].open()
		else:
			OUTPUTS[valve].close()
	if stats["Ignition"]:
		OUTPUTS["Ignition"].start()

while True:
        dic = {'load' : 0.0, 'pressure' : 0.0, 'thermo' : 0.0}
        data = json.dumps(dic)
        print "DATA:\n"
        print data
        connection.send(data)
        print "good"
        received = connection.recv(1028)
        print "RECEIVED:\n"
        print received
        stats = json.loads(received)
        print "STATUS:\n"
        print stats
        update_outputs(stats)