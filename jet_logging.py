#!/usr/bin/env python3
import board
import busio
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
import Adafruit_ADS1x15 as ADS
import time
import os
import glob
from mqtt_client.publisher import Publisher
import json
from threading import Thread
import sys, traceback

try:
	# Setup Current Sensors
	i2c = busio.I2C(board.SCL, board.SDA)

	ads = ADS.ADS1115(address=0x48)
	ads.gain = 1
	chan = AnalogIn(ads, ADS.P0) #current 1
	chan2 = AnalogIn(ads,ADS.P1) #current 2
	chan3 = AnalogIn(ads, ADS.P2) #pack voltage
	chan4 = AnalogIn(ads, ADS.P3) #comp temp

	# Setup Temperature Sensors
	ads_temp = ADS.ADS1115(address=0x49)
	ads_temp.gain = 1
	temp1 = AnalogIn(ads_temp, ADS.P0)
	temp2 = AnalogIn(ads_temp, ADS.P1)
	temp3 = AnalogIn(ads_temp, ADS.P2)
	temp4 = AnalogIn(ads_temp, ADS.P3)

except Exception:
	traceback.print_exc(file=sys.stdout)
#        pass

#Temperature global variables
#temp1 = 0
#temp2 = 0
#temp3 = 0
#temp4 = 0
#chan = 0
#chan2 = 0
#chan3 = 0
#chan4 = 0

# Setup Pubber
pubber = Publisher(client_id="jet-pubber")

def log_temp_current():
	while True:
		try:
			publish_adc_status()
			publish_temp_status()
			time.sleep(.1)
		except Exception:
                    #    print('error')
                        traceback.print_exc(file=sys.stdout)
			#pass


def publish_temp_status():
		
	global temp1
	global temp2
	global temp3
	global temp4

	# convert input voltage in mV to temperature in centigrade
	jet1_temp = ((temp1.voltage * 1000) - 500)/10
	jet2_temp = ((temp2.voltage * 1000) - 500)/10
	jet3_temp = ((temp3.voltage * 1000) - 500)/10
	jet4_temp = ((temp4.voltage * 1000) - 500)/10
	
	message = {
			'jet1_temp' : str(jet1_temp),
			'jet2_temp': str(jet2_temp),
			'jet3_temp' : str(jet3_temp),
			'jet4_temp' : str(jet4_temp)

	}
	print(message)
	# app_json = json.dumps(message)
	# pubber.publish("/status/temp",app_json)

def publish_adc_status():

	global chan
	global chan2
	global chan3
	global chan4

	jet1_amps = ((chan.voltage - 2.47) / 0.013)
	jet2_amps = ((chan2.voltage - 2.47) / 0.013)
	pack_voltage = round((chan3.voltage * 5),2)
	MPA_temp = round((chan4.voltage * 1000) - 500)/10

	message = {
		'jet1_amps': jet1_amps,
		'jet2_amps': jet2_amps,
		'pack_voltage' : pack_voltage,
		'MPA_temp' : MPA_temp
	}
	print(message)
	app_json = json.dumps(message)
	pubber.publish("/status/adc",app_json)

# MAIN METHOD

thread = Thread(target=log_temp_current)
thread.start()


