from jet import Jet
from jet_logging import * #this starts and runs the logging for the jets
from mqtt_client.subscriber import Subscriber
from threading import Thread
import json
import time

#global varriables for subscriptions
cur_speed = 0
gps_course = 0
target_heading = 0
magnitude = 0

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
    target_heading = obj["heading"]
    gps_course = obj["magnitude"]


def main():
    

    


if __name__ == "__main__":
    Jet1 = Jet(False)
    Jet2 = Jet(True)

    Jet1.startup()
    Jet2.startup()

    Jet1.zero()
    Jet2.zero()

    try:
        default_subscriptions = {
            "/status/gps" : on_gps_received
            "/status/vector" : on_vector_received
        }
        subber = Subscriber(client_id="jet_ctrl_id", broker_ip="192.168.1.170", default_subscriptions=default_subscriptions)
        thread = Thread(target=subber.listen)
        thread.start()
    except Exception:
        print("Subcribing to /gps or /vector failed") 

    main()