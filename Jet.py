from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

class Jet:

    def __init__(self, port_jet):
        self.port_jet = port_jet
        if port_jet == False: #Jet1 Starboard Jet
            ESC1 = kit.servo[4]
            RB1 = kit.servo[5]
            DIR1 = kit.servo[6]
        if port_jet == True: #Jet2 Port Jet
            ESC2 = kit.servo[0]
            RB2 = kit.servo[1]
            DIR2 = kit.servo[2]

Jet1 = Jet(False)
Jet2 = Jet(True)

print("Jet 1 is Starboard, so False..." + Jet1.port_jet)