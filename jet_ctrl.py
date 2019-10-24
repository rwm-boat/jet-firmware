from jet import Jet
from jet_logging import * #this starts and runs the logging for the jets
from mqtt_client.subscriber import Subscriber
from threading import Thread
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

speed_state = -1

Jet1 = Jet(False)
Jet2 = Jet(True)

def calc_speed_state():
    if cur_speed < 0.5 and jet1_current+jet2_current < 5:
        speed_state = 0 #stopped
        print("speed_state: stopped")
    if 0.5 <= cur_speed < 7.5:
        speed_state = 1 #trolling
        print("speed_state: trolling")
    if 7.5 <= cur_speed:
        speed_state = 2 #on plane
        print("speed_state: on-plane")

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

def on_vector_received(client, userdata, message):
    global target_heading
    global magnitude

    obj = json.loads(message.payload.decode('utf-8'))
    target_heading = float(obj["heading"])
    gps_course = float(obj["magnitude"])

    calc_speed_state() 
    main_switch(speed_state)

def main_switch(speed_state):
    switcher = {
        0: print("In Stopped State"),
        1: print("In Trolling State"),
        2: print("In On-Plane State")
    }
    print(switcher.get(speed_state, "Invalid Speed State"))

def init_jets():
    
    Jet1.startup()
    Jet2.startup()

    Jet1.zero()
    Jet2.zero()

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

    Jet1.th_rq(10)
    Jet1.rb_rq('down')