import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import os
import glob
from mqtt_client.publisher import Publisher
import json
from w1thermsensor import  W1ThermSensor


# Setup ADC Sensor
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads,ADS.P1)

# Setup Pubber
pubber = Publisher(client_id="jet-pubber")
temp_f7 = 0
temp_b9 = 0
temp_f0 = 0

def publish_temp_status():
		
		global temp_f7
		global temp_b9
		global temp_f0

		for sensor in W1ThermSensor.get_available_sensors():
		    if(sensor.id == "28-030197944df7"):
		        temp_f7 = sensor.get_temperature()
		    elif(sensor.id == "28-0307979401b9"):
			temp_b9 = sensor.get_temperature()
		    else:
		        temp_f0 = sensor.get_temperature
				
        message = {
	    'temp_jet1' : temp_f7,
	    'temp_jet2': temp_f0,
	    'compartment_temp' : temp_b9
        }
	print(message)
	app_json = json.dumps(message)
	pubber.publish("/status/temp",app_json)

def publish_adc_status():

	jet1_amps = ((chan.voltage - 2.47) / 0.013) * 100
	jet2_amps = ((chan2.voltage - 2.47) / 0.013) * 100

	message = {
		'jet1_amps': jet1_amps,
		'jet2_amps': jet2_amps
	}
	print(json.dumps(message))
	app_json = json.dumps(message)
	pubber.publish("/status/adc",app_json)

while(True):
	publish_temp_status()
	publish_adc_status()
	time.sleep(1)

