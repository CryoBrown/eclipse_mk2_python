import outputs
import time

FILLPIN = 19
RELIEFPIN = 16
VENTPIN = 26
IGNITIONPIN = 20

VALVE_FILL = outputs.BallValve(FILLPIN)
#VALVE_VENT = outputs.BallValve(VENTPIN)

#VALVE_RELIEF = outputs.ServoValve(RELIEFPIN)

#Ignition
#OUTPUT_IGNITION = outputs.Ignition(IGNITIONPIN)

while(True):
    print "Open"
    VALVE_FILL.open()
    time.sleep(3)
    print "Close"
    VALVE_FILL.close()
    time.sleep(3)