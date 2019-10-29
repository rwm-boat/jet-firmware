#!/usr/bin/env python3
from jet import Jet
from jet_logging import * #this starts and runs the logging for the jets
from mqtt_client.subscriber import Subscriber
from threading import Thread
from simple_pid import PID
import json
import time

#global varriables
cur_speed = 0
gps_course = 0
target_heading = 0
magnitude = 0
jet1_current = 0
jet2_current = 0
pack_voltage = 0

speed_state = 0
heading_delta = 0

follow_course = False

course_degree_tolerence = 20

Jet1 = Jet(False)
Jet2 = Jet(True)    

heading_hold_pid = PID(1, 0.1, 0.05)
dir_tune = 0.5

def on_adc_received(client, userdata, message):
    global jet1_current
    global jet2_current
    global pack_voltage

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = float(obj["jet1_amps"])
    jet2_current = float(obj["jet2_amps"])
    pack_voltage = float(obj['pack_voltage'])

def on_gps_received(client, userdata, message):
    # create global variables for UI
    global cur_speed
    global gps_course
    
    obj = json.loads(message.payload.decode('utf-8'))
    cur_speed = obj["speed"]
    gps_course = obj["course"]
    try:
        cur_speed = float(cur_speed)
        gps_course = float(gps_course)
    except Exception:
        print("Invalid input from gps")

def on_vector_received(client, userdata, message):
    global target_heading
    global magnitude
    global heading_delta
    global follow_course

    obj = json.loads(message.payload.decode('utf-8'))
    target_heading = float(obj["heading"])
    magnitude = float(obj["magnitude"])

    heading_hold_pid.setpoint = target_heading

    calc_speed_state()

    # heading_delta = target_heading - gps_course
    print("Vector Received")

    if not magnitude == 0:
        follow_course = True
    else:
        follow_course = False

    # main_switch(speed_state)    

def calc_speed_state():
    global speed_state
    print("Jet1 current = %s" %(jet1_current))
    print("Jet2 current = %s" %(jet2_current))
    print("Speed = %s" %(cur_speed))
    if cur_speed < 1.0 and jet1_current + jet2_current < 5: 
        speed_state = 0 #stopped
        print("speed_state: stopped")
    if 1.0 <= cur_speed < 7.5 and 10 > 5: #jet1_current + jet2_current
        speed_state = 1 #trolling
        print("speed_state: trolling")
    if 7.5 <= cur_speed and jet1_current + jet2_current > 60:
        speed_state = 2 #on plane
        print("speed_state: on-plane")
    
    if magnitude == 0:
        speed_state = 0

def stopped_state():
    print("State: Stopped")
    #for now, when we get a new vector while stopped,
    #we will drive straight slowly until a gps_course is 
    #accuratly aquired
    if magnitude == 0:
        Jet1.th_rq(0)
        Jet2.th_rq(0)
    else:
        # Jet1.th_rq(15)
        # Jet2.th_rq(15)
        print("Jets moving at 15")
        print("Moving to acquire gps_course and gain speed")
        # calc_speed_state()
        # main_switch(speed_state) 
        
        #this will loop until it's put in the trolling state

def trolling_state():
    global follow_course
    global heading_delta
    global target_heading
    global gps_course

    print("State: Trolling")
    # Jet1.th_rq(magnitude*20) #change later to a speed target for trolling
    # Jet2.th_rq(magnitude*20) #use pid to hit target speed, magnitude will corelate to target speed
    print("Jets moving at trolling speed")
    
    heading_delta = target_heading - gps_course
    
    if heading_delta < 0 and abs(heading_delta) > 180:
        heading_delta = 360 - abs(heading_delta)
    if heading_delta > 0 and heading_delta > 180:
        heading_delta = heading_delta - 360

    if heading_delta > 0:
        Jet1.dir_rq(-heading_delta*dir_tune)
        Jet2.dir_rq(-heading_delta*dir_tune)
        print("Follow Course-- turn right %s degrees" %(heading_delta))
    if heading_delta < 0:
        Jet1.dir_rq(heading_delta*dir_tune)
        Jet2.dir_rq(heading_delta*dir_tune)
        print("Follow Course-- turn left %s degrees" %(heading_delta))
    
    
def onplane_state():
    print("State: On-Plane")

def main_switch(speed_state):
    switcher = {
        0: stopped_state,
        1: trolling_state,
        2: onplane_state
    }
    function = switcher.get(speed_state, "Invalid Speed State")
    function()

def init_jets():
    
    Jet1.startup()
    Jet2.startup()

    Jet1.zero()
    Jet2.zero()

def main_switch_runner():
    while(True):
        main_switch(speed_state)
        time.sleep(0.1)

def main():
    try:
        default_subscriptions = {
            "/status/gps" : on_gps_received,
            "/status/vector" : on_vector_received,
            "/status/adc" :on_adc_received
        }
        subber = Subscriber(client_id="jet_ctrl_id", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()
    except Exception:
        print("--!!Subcribing to /gps or /vector failed!!--") 
    
if __name__ == "__main__":
    
    init_jets()
    main()

    main_thread = Thread(target=main_switch_runner())
    main_thread.start()


    