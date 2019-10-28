#!/usr/bin/env python3
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import os
import glob
from mqtt_client.publisher import Publisher
import json
from threading import Thread


# Setup Current Sensors
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c, address=0x48)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads,ADS.P1)
chan3 = AnalogIn(ads, ADS.P2)

# Setup Temperature Sensors
ads_temp = ADS.ADS1115(i2c, address=0x49)
ads_temp.gain = 1
jet1_in = AnalogIn(ads_temp, ADS.P0)
jet2_in = AnalogIn(ads_temp, ADS.P1)
compartment_in = AnalogIn(ads_temp, ADS.P2)

# Temperature global variables
jet1_temp = 0
jet2_temp = 0
compartment_temp = 0

# Setup Pubber
pubber = Publisher(client_id="jet-pubber")

def log_temp_current():
	while True:
		try:
			publish_adc_status()
			publish_temp_status()
			time.sleep(.1)
		except Exception:
			print("no temp or current sensors")

def publish_temp_status():
		
	global jet1_temp
	global compartment_temp
	global jet2_temp

	# convert input voltage in mV to temperature in centigrade
	jet1_temp = ((jet1_in.voltage * 1000) - 500)/10
	jet2_temp = ((jet2_in.voltage * 1000) - 500)/10
	compartment_temp = ((compartment_in.voltage * 1000) - 500)/10
	
	message = {
			'jet1_temp' : str(jet1_temp),
			'jet2_temp': str(jet2_temp),
			'compartment_temp' : str(compartment_temp)
	}
	print(message)
	app_json = json.dumps(message)
	pubber.publish("/status/temp",app_json)

def publish_adc_status():

	jet1_amps = ((chan.voltage - 2.47) / 0.013)
	jet2_amps = ((chan2.voltage - 2.47) / 0.013)
	pack_voltage = round((chan3.voltage * 5),2)

	message = {
		'jet1_amps': jet1_amps,
		'jet2_amps': jet2_amps,
		'pack_voltage' : pack_voltage
	}
	print(json.dumps(message))
	app_json = json.dumps(message)
	pubber.publish("/status/adc",app_json)

# MAIN METHOD

thread = Thread(target=log_temp_current)
thread.start()


