#!/usr/bin/env python3
from jet import Jet
from jet_logging import * #this starts and runs the logging for the jets
from mqtt_client.subscriber import Subscriber
from threading import Thread
from simple_pid import PID
import json
import time
import numpy as np 


#global varriables
gps_speed = 0
gps_course = 0
target_heading = -1
magnitude = 0
jet1_current = 0
jet2_current = 0
pack_voltage = 0
mag_compass = 0

speed_state = 0
heading_delta = 0
heading_delta_avg = 0

th_request = 0

SLOW_SPEED = 1.0
TROLL_SPEED = 2.2
HULL_SPEED = 4.5
MIN_PLANE_SPEED = 8.0
MAX_SPEED = 11.0

hd_array = []
turn = False
go_straight = False

KD_SPEED = 10
MVING_AVG_N = 30 # heading_delta moving average count
GO_STRAIGHT_HOLD = 20 # scalar (_delta / go_straight_hold)
STRAIGHT_TURN_TOL = 70 # degrees 
GO_STRAIGHT_LOOP_SPEED = 1 # seconds
KD_DIR = 0.5 # DIR tune
TURN_TOL = 15 # degrees

Jet1 = Jet(False)
Jet2 = Jet(True)    


def on_compass_received(client, userdata, message):
    global mag_compass
    obj = json.loads(message.payload.decode('utf-8'))
    mag_compass = obj['compass']

    try:
        mag_compass = float(mag_compass)
    except Exception:
        print("Invalid Compass Reading")

def on_adc_received(client, userdata, message):
    global jet1_current
    global jet2_current
    global pack_voltage

    obj = json.loads(message.payload.decode('utf-8'))
    jet1_current = float(obj["jet1_amps"])
    jet2_current = float(obj["jet2_amps"])
    pack_voltage = float(obj['pack_voltage'])

def on_gps_received(client, userdata, message):
    global gps_speed
    global gps_course
    
    obj = json.loads(message.payload.decode('utf-8'))
    gps_speed = obj["speed"]
    gps_course = obj["course"]
    try:
        gps_speed = float(gps_speed)
        gps_course = float(gps_course)
    except Exception:
        print("Invalid input from gps")

def on_vector_received(client, userdata, message):
    global target_heading
    global magnitude

    obj = json.loads(message.payload.decode('utf-8'))
    target_heading = float(obj["heading"])
    magnitude = float(obj["magnitude"])
    print("Vector Received")

    if target_heading == 0 and magnitude == 0:
        print("Waypoint hit")
        #TODO
        # What is the boat going to do when waypoint is hit 

def calc_heading_delta():
    global heading_delta
    global heading_delta_avg
    global hd_array
    
    heading_delta = target_heading - gps_course

    # Fixes 360 errors (_delta is saying to turn left or right 180 degrees)
    # -90 turn left, 90 turn right
    if heading_delta < 0 and abs(heading_delta) > 180:
        heading_delta = 360 - abs(heading_delta)
    if heading_delta > 0 and heading_delta > 180:
        heading_delta = heading_delta - 360

    if len(hd_array) < MVING_AVG_N:
        hd_array.append(heading_delta)
    else:
        del hd_array[0]
        hd_array.append(heading_delta)
    heading_delta_avg = round(sum(hd_array)/len(hd_array),1)
    
    # print("Target Heading = %s" %(target_heading))
    # print("GPS Course  = %s" %(gps_course))
    # print("Mag Compass = %s" %(mag_compass))
    # print("Heading Delta = %s" %(heading_delta))
    # print("Heading Delta AVG = %s" %(heading_delta_avg))

def speed_ctrl():
    global th_request
    target_speed = 0
    
    if magnitude == 0: target_speed = 0
    if magnitude == 1: target_speed = SLOW_SPEED
    if magnitude == 2: target_speed = TROLL_SPEED 
    if magnitude == 3: target_speed = HULL_SPEED
    if magnitude == 4: target_speed = MIN_PLANE_SPEED
    if magnitude == 5: target_speed = MAX_SPEED
    
    Jet1.th_rq(magnitude*12)
    Jet2.th_rq(magnitude*12)


def calc_speed_state():
    global speed_state

    print("Speed = %s" %(gps_speed))
    if gps_speed < 0.3 and jet1_current + jet2_current < 5: 
        speed_state = 0 #stopped
        print("speed_state: stopped")
    if 0.3 <= gps_speed < 7.5 and jet1_current + jet2_current > 5: #jet1_current + jet2_current
        speed_state = 1 #trolling
        print("speed_state: trolling")
    if 7.5 <= gps_speed and jet1_current + jet2_current > 60:
        speed_state = 2 #on plane
        print("speed_state: on-plane")
    
    if magnitude == 0:
        speed_state = 0


def execute():
    global turn
    global go_straight
    
    # if abs(heading_delta) < STRAIGHT_TURN_TOL:
    #     turn = False
    #     go_straight = True

    go_straight = True
    if abs(heading_delta_avg) > STRAIGHT_TURN_TOL:
        go_straight = False
        turn = True

    if go_straight:

        if heading_delta_avg > 10: # need to go right
            print("Go Straight++ %s degrees" %(heading_delta_avg))
            Jet1.dir_rq(heading_delta_avg*KD_DIR)
            Jet2.dir_rq(heading_delta_avg*KD_DIR)

            time.sleep(abs(heading_delta_avg)/GO_STRAIGHT_HOLD)
            Jet1.dir_rq(0)
            Jet2.dir_rq(0)

        elif heading_delta_avg < -10: # need to go left
            print("Go Straight-- %s degrees" %(heading_delta_avg))
            Jet1.dir_rq(heading_delta_avg*KD_DIR)
            Jet2.dir_rq(heading_delta_avg*KD_DIR)

            time.sleep(abs(heading_delta_avg)/GO_STRAIGHT_HOLD)
            Jet1.dir_rq(0)
            Jet2.dir_rq(0)

        else:
            Jet1.dir_rq(0)
            Jet2.dir_rq(0)
        
        time.sleep(GO_STRAIGHT_LOOP_SPEED)
           
    if turn:
        print("Starting Turn")
        turn_amount = heading_delta_avg
        mag_home = mag_compass
        mag_target = mag_home + turn_amount

        if mag_target < 0:
            mag_target = mag_target + 360
        if mag_target > 360:
            mag_target = mag_target - 360

        if turn_amount > 0: #turn right
            while mag_compass < mag_target - TURN_TOL:
                Jet1.dir_rq((mag_target-mag_compass)*KD_DIR)
                Jet2.dir_rq((mag_target-mag_compass)*KD_DIR)
                print("Turning Right %s" %(mag_target-mag_compass))
                time.sleep(0.2)
            Jet1.dir_rq(0)
            Jet2.dir_rq(0)
            turn = False
            go_straight = True
        
        if turn_amount < 0: #turn left
            while mag_compass > mag_target + TURN_TOL:
                Jet1.dir_rq((mag_target-mag_compass)*KD_DIR)
                Jet2.dir_rq((mag_target-mag_compass)*KD_DIR)
                print("Turning Left %s" %(mag_target-mag_compass))
                time.sleep(0.2)
            Jet1.dir_rq(0)
            Jet2.dir_rq(0)
            turn = False
            go_straight = True

def execute_runner():
    while(True):
        execute()
        time.sleep(0.2)

def calc_heading_delta_runner():
    while(True):
        calc_heading_delta()
        time.sleep(0.1)

def speed_ctrl_runner():
    while(True):
        speed_ctrl()
        time.sleep(1)

def main():
    try:
        default_subscriptions = {
            "/status/compass": on_compass_received,
            "/status/gps" : on_gps_received,
            "/status/vector" : on_vector_received,
            "/status/adc" :on_adc_received
        }
        subber = Subscriber(client_id="jet_ctrl_id", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()
    except Exception:
        print("--!!Subcribing to /gps or /vector or /adc failed!!--") 
    
if __name__ == "__main__":
    
    Jet1.zero()
    Jet2.zero()

    main()

    heading_delta_thread = Thread(target=calc_heading_delta_runner)
    speed_ctrl_thread = Thread(target=speed_ctrl_runner)
    main_thread = Thread(target=execute_runner)
    
    heading_delta_thread.start()
    speed_ctrl_thread.start()
    main_thread.start()


    