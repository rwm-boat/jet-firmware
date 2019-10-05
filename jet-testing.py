import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import os
import glob
from mqtt_client.publisher import Publisher
import json

# Setup Temp Sensor
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')
 
# base_dir = '/sys/bus/w1/devices/'
# device_folder = glob.glob(base_dir + '28*')[0]
# device_file = device_folder + w1_slave'

# Setup ADC Sensor
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads,ADS.P1)
# Setup Pubber
pubber = Publisher(client_id="jet-pubber")

# def read_temp_raw():
#     f = open(device_file, 'r')
#     lines = f.readlines()
#     f.close()
#     return lines
 
# def read_temp():
#     lines = read_temp_raw()
#     while lines[0].strip()[-3:] != 'YES':
#         time.sleep(0.2)
#         lines = read_temp_raw()
#     equals_pos = lines[1].find('t=')
#     if equals_pos != -1:
#         temp_string = lines[1][equals_pos+2:]
#         temp_c = float(temp_string) / 1000.0
#         temp_f = temp_c * 9.0 / 5.0 + 32.0
#         return temp_c, temp_f

# Typical reading
# 73 01 4b 46 7f ff 0d 10 41 : crc=41 YES
# 73 01 4b 46 7f ff 0d 10 41 t=23187

while True:

	for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
		id = sensor.split("/")[5]

		try:
			f = open(sensor, "r")
			data = f.read()
			f.close()
			if "YES" in data:
			(discard, sep, reading) = data.partition(' t=')
			t = float(reading) / 1000.0
			print("{} {:.1f}".format(id, t))
			else:
			print("999.9")

		except:
			pass

def publish_temp_status():
	temp_c, temp_f = readTemp()
	message = {
		'temp_c' : temp_c,
		'temp_f': temp_f,
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
	#publish_temp_status()
	publish_adc_status()
	time.sleep(1)

