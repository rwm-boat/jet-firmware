#!/usr/bin/env python3
from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

#negative -> trim right
#positive -> trim left
DIR1_offset = -5
DIR2_offset = 0

DIR_limit = 25

ESC1 = kit.servo[4]
RB1 = kit.servo[5]
DIR1 = kit.servo[6]

ESC2 = kit.servo[0]
RB2 = kit.servo[1]
DIR2 = kit.servo[2]

class Jet:

    def __init__(self, port_jet):
        self.port_jet = port_jet
        if port_jet == False: #Jet1 Starboard Jet
            #ESC PWM assign
            ESC1.actuation_range = 180 
            ESC1.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC
            #RB PWM assign
            RB1.actuation_range = 180
            RB1.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            #DIR PWM assign
            DIR1.actuation_range = 180
            DIR1.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            print("Jet 1 Init")
            
        if port_jet == True: #Jet2 Port Jet
            #ESC PWM assign
            ESC2.actuation_range = 180 
            ESC2.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC
            #RB PWM assign
            RB2.actuation_range = 180
            RB2.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            #DIR PWM assign
            DIR2.actuation_range = 180
            DIR2.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            print("Jet 2 Init")
        
    #--end Jet init--
    
    def zero(self):
        if self.port_jet: #port jet
            self.th_rq(0)
            self.rb_rq('up')
            self.dir_rq(0)
            print("Jet 2 Zeroed")
        else:            #starboard jet
            self.th_rq(0)
            self.rb_rq('up')
            self.dir_rq(0)
            print("Jet 1 Zeroed")
    #--end zero--
    
    def th_rq(self, mag):
        if mag > 100:
            mag = 100
            print("Throttle mag limited to 100")
        if mag < 0:
            print("Throttle mag needs to be positive")

        vel = ((mag)*18)/10 #converts mag into a pwm value

        #math to keep pwm values within usable range
        if vel < 10 and vel > 0:
            vel = 10
        if vel > 180:
            vel = 180
        #--end of math

        if self.port_jet: #port jet
            ESC2.angle = vel
            print("Jet 2 set th_rq: %s" %(mag))
        else:             #stardboard jet
            ESC1.angle = vel
            print("Jet 1 set th_rq: %s" %(mag))
    #--end th_rq--

    def rb_rq(self,level):
        if level == 'down':
            pos = 20
        if level == 'mid':
            pos = 70
        if level == 'up':
            pos = 130
        
        if self.port_jet: #port jet
            RB2.angle = pos
            print("Jet 2 set rb_rq: " + level)
        else:             #starboard jet
            RB1.angle = pos
            print("Jet 1 set rb_rq: " + level)
    #--end rb_rq--

    def dir_rq(self,angle): #range is 25 to -25 degrees (phyiscally)
        if angle > DIR_limit:
            angle = DIR_limit
            #print("Director limited to 25")
        if angle < -DIR_limit:
            angle = -DIR_limit
            #print("Director limited to -25")

        if self.port_jet: #port jet
            dir2PWM = 90 + DIR2_offset + angle
            DIR2.angle = dir2PWM
            print("Jet 2 set dir_rq: %s" %(angle))
        else:
            dir1PWM = 90 + DIR1_offset + angle
            DIR1.angle = dir1PWM
            print("Jet 1 set dir_rq: %s" %(angle))
    #--end dir_rq--

    def startup(self):
        self.rb_rq('down')
        time.sleep(0.5)
        self.rb_rq('up')
        time.sleep(0.5)

        self.dir_rq(25)
        time.sleep(0.5)
        self.dir_rq(-25)
        time.sleep(0.5)
        self.dir_rq(0)

        self.th_rq(10)
        time.sleep(0.25)
        self.th_rq(0)



