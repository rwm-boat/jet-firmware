from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

DIR1_offset = 0
DIR2_offset = 0

class Jet:

    def __init__(self, port_jet):
        self.port_jet = port_jet
        if port_jet == False: #Jet1 Starboard Jet
            self.ESC1 = kit.servo[4]
            self.RB1 = kit.servo[5]
            self.DIR1 = kit.servo[6]
            
        if port_jet == True: #Jet2 Port Jet
            self.ESC2 = kit.servo[0]
            self.RB2 = kit.servo[1]
            self.DIR2 = kit.servo[2]
            
        
    #--end Jet init--
    
    def setup(self):
        if self.port_jet: #port jet
            #ESC PWM assign
            ESC2.actuation_range = 180 
            ESC2.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC
            #RB PWM assign
            RB2.actuation_range = 180
            RB2.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            #DIR PWM assign
            DIR2.actuation_range = 180
            DIR2.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            Jet2.th_rq(0)
            Jet2.rb_rq('up')
            Jet2.dir_rq(0)
            print("Jet 2 (Port) ESC ARMED")
        else:            #starboard jet
            #ESC PWM assign
            ESC1.actuation_range = 180 
            ESC1.set_pulse_width_range(930,2300) #correct microsecond range for Turnigy 70A ESC
            #RB PWM assign
            RB1.actuation_range = 180
            RB1.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            #DIR PWM assign
            DIR1.actuation_range = 180
            DIR1.set_pulse_width_range(500, 2400) #correct microsecond range for DS3218mg servos
            Jet1.th_rq(0)
            Jet1.rb_rq('up')
            Jet1.dir_rq(0)
            print("Jet 1 (Starboard) ESC ARMED")

        time.sleep(5) #time for ESCs to arm
        
        
    #--end setup--
    
    def th_rq(self, mag):
        if mag > 100:
            mag = 100
            print("Throttle mag limited to 100")

        if mag < 0:
            print("Throttle mag needs to be positive")

        vel = ((abs(mag))*18)/10 #converts mag into a pwm value

        #math to keep pwm values within usable range
        if vel < 10 and vel > 0:
            vel = 10

        if vel > 180:
            vel = 180
        #--end of math

        if self.port_jet: #port jet
            ESC2.angle = vel
        else:             #stardboard jet
            ESC1.angle = vel

    #--end th_rq--

    def rb_rq(self,level):
        if level == 'down':
            pos = 20
        if level == 'mid':
            pos = 75
        if level == 'up':
            pos = 100
        
        if self.port_jet: #port jet
            RB2.angle = pos
        else:             #starboard jet
            RB1.angle = pos

    #--end rb_rq--

    def dir_rq(self,angle): #range is 25 to -25 degrees (phyiscally)
        if angle > 25:
            angle = 25
            print("Director limited to 25")

        if angle < -25:
            angle = -25
            print("Director limited to -25")


        if self.port_jet: #port jet
            DIR2.angle = 90 + DIR2_offset + angle
        else:
            DIR1.angle = 90 + DIR1_offset + angle
    
    #--end dir_rq--


#Brent's basic testing
Jet1 = Jet(True)
Jet2 = Jet(False)

Jet1.rb_rq('down')
Jet2.rb_rq('down')

