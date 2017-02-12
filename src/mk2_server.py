import socket
import json

import time

import outputs
import Adafruit_ADS1x15

from optparse import OptionParser

#Get Options from the command line
parser = OptionParser()

parser.add_option('--s', action="store", dest="server", help="ip address", default = "127.0.0.1")
parser.add_option('--c', action="store", dest="client", help="ip address", default = "127.0.0.1")
options, args = parser.parse_args()
print "SERVER IP:", options.server
print "CLIENT IP:", options.client


#Get Addresses
address_me = (options.server, 5004)
address_u = (options.client, 5005)


#Initialize DGRAM socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind(address_me)
serversocket.settimeout(0.5)


#Pin
FILLPIN = 13
VENTPIN = 26

RELIEFENABLEPIN = 16
RELIEFPIN = 4

IGNITIONPIN = 18
HEATERENABLEPIN = 23

#Valves
VALVE_FILL = outputs.BallValve(FILLPIN)
VALVE_VENT = outputs.BallValve(VENTPIN)

VALVE_RELIEF = outputs.ServoValve(RELIEFPIN)
RELIEF_ENABLE = outputs.Enable(RELIEFENABLEPIN)

#Heater
HEATER_ENABLE = outputs.Enable(HEATERENABLEPIN)

#Ignition
OUTPUT_IGNITION = outputs.Ignition(IGNITIONPIN)

VALVE_TITLES = ('fill', 'relief', 'vent')

DEFAULT_STATUSES = {'fill':False, 'relief':True, 'vent':False, 'ignition':False, 'relief_enable':True, 'heater_enable':False}
statuses = {'fill':True, 'relief':False, 'vent':True, 'ignition':True, 'relief_enable':False, 'heater_enable':True}

OUTPUTS = {'fill':VALVE_FILL, 'relief':VALVE_RELIEF, 'vent':VALVE_VENT, 'ignition':OUTPUT_IGNITION,
           'relief_enable':RELIEF_ENABLE, 'heater_enable':HEATER_ENABLE}



adc = Adafruit_ADS1x15.ADS1015()
GAIN = 1

def read_instruments(adc):
    readings = {}
    readings["load"] = adc.read_adc(0, gain=GAIN)
    readings["pressure"] = adc.read_adc(1, gain=GAIN)
    readings["thermo"] = 0.0
    return readings


def update_outputs(stats):
    for valve in VALVE_TITLES:
        if stats[valve] != statuses[valve]:
            statuses[valve] = stats[valve]
        if statuses[valve]:
            OUTPUTS[valve].open()
        else:
            OUTPUTS[valve].close()
    if stats["ignition"] != statuses["ignition"]:
        statuses["ignition"] = stats["ignition"]
        if statuses["ignition"]:
            OUTPUTS["ignition"].start()
        else:
            OUTPUTS["ignition"].stop()
    if stats["heater_enable"] != statuses["heater_enable"]:
        statuses["heater_enable"] = stats["heater_enable"]
        if statuses["heater_enable"]:
            OUTPUTS["heater_enable"].enable()
        else:
            OUTPUTS["heater_enable"].disable()
    if stats["relief_enable"] != statuses["relief_enable"]:
        statuses["relief_enable"] = stats["relief_enable"]
        if statuses["relief_enable"]:
            OUTPUTS["relief_enable"].enable()
        else:
            OUTPUTS["relief_enable"].disable()



dic = {'load' : 0.0, 'pressure' : 0.0, 'thermo' : 0.0}
data = json.dumps(dic)

update_outputs(DEFAULT_STATUSES)

i = 0
while True:
        #print "----------------------------------------------"
        #print "BEGIN LOOP " + str(i)
        #print "\n"
	#print i 

        data = json.dumps(read_instruments(adc))

        #print "SENDING..."
        try:
            serversocket.sendto(data, address_u)
            #print "done."
        except StandardError:
            #print "failed."
            pass
       # print "\n"

        #print "RECEIVING..."
        try:
            received, addr = serversocket.recvfrom(1024)
            #print "done."
            stats = json.loads(received)
            #print "UPDATING OUTPUTS"
            update_outputs(stats)
            #print "done."
        except StandardError:
            pass
            #print "failed"

        #print "END LOOP " + str(i)
        #print "----------------------------------------------\n"
        i+=1
