#! /usr/bin/python3
from jet import Jet
import time
import sys
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import glob
import json
from threading import Thread
from datetime import datetime

EMULATE_HX711=False

Jet = Jet(True)

#### --------- Calibration ---------------####

referenceUnit = -858.66

#### -------------------------------------####

adc_current = 0

thrust_arr = []
current_arr = []

if not EMULATE_HX711:
	import RPi.GPIO as GPIO
	from hx711 import HX711
else:
	from emulated_hx711 import HX711

def setup():
	global adc_current
	try:
		# Setup Current Sensors
		i2c = busio.I2C(board.SCL, board.SDA)
		ads = ADS.ADS1115(i2c, address=0x48)
		ads.gain = 1
		adc_current = AnalogIn(ads, ADS.P0)
		adc_temp1 = AnalogIn(ads,ADS.P1)
		adc_temp2 = AnalogIn(ads, ADS.P2)
		adc_temp3 = AnalogIn(ads, ADS.P3)
	except Exception:
		print("ADC startup failed")

def run_test():
		for x in range(0,100):
			Jet.th_rq(x)
			time.sleep(0.1)

def cleanAndExit():
	print("Cleaning...")

	if not EMULATE_HX711:
		GPIO.cleanup()
		
	print("Bye!")
	sys.exit()

### Initialize HX711 and ADC
setup()
### Initialize HX7111 with RPI pinout
hx = HX711(5, 6)
### Set order of bytes received, works for now, don't touch
hx.set_reading_format("MSB", "MSB")
### Set reference unit determined by calibration procedure
hx.set_reference_unit(referenceUnit)
### Tare scale before using
hx.reset()
hx.tare()
print("Tare done! Add weight now...")


Jet.zero()
time.sleep(5)
# Jet.th_rq(10)
# time.sleep(1)
# Jet.zero()



time_now = datetime.today()
log_time = (
		f"{time_now.year}-{time_now.month}-{time_now.day}-{time_now.hour}:{time_now.minute}:{time_now.second}"
		)
counter = 0
while True:
	try:
		jet_amps = ((adc_current.voltage - 2.47) / 0.013)
		jet_thrust = hx.get_weight(5)
		print("Grams Thrust: ", round(jet_thrust,3), "  Jet Current: ", round(jet_amps,3), " Throttle Request: ", counter)
		message = {
			'thrust' : jet_thrust,
			'current' : jet_amps
		}
		app_json = json.dumps(message)
		with open(f"../logs/{log_time}.txt", "a") as outfile:
			json.dump(message, outfile)
			outfile.write("\n")
			thrust_arr.append(jet_thrust)
			current_arr.append(jet_amps)
		time.sleep(0.1)
	
		counter +=1
		if(counter is not 50):
			Jet.th_rq(counter)
		else:
			Jet.zero()
			exit()			
		time.sleep(0.2)
		
	except (KeyboardInterrupt, SystemExit):
		print("Max Thrust (grams): ", max(thrust_arr))
		print("Max Current (amps): ", max(current_arr))
		cleanAndExit()
