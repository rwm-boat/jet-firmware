from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)

DIR1_offset = 0
DIR2_offset = 0

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
            print("Starboard Jet Init")
            
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
            print("Port Jet Init")
        
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
        else:             #stardboard jet
            ESC1.angle = vel
    #--end th_rq--

    def rb_rq(self,level):
        if level == 'down':
            pos = 20
        if level == 'mid':
            pos = 60
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

def main():
    Jet1 = Jet(False)
    Jet2 = Jet(True)

    Jet1.zero()
    Jet2.zero()

if __name__ == "__main__":
    main()


