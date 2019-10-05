import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import os
import glob
from mqtt_client.publisher import Publisher
import json

#base directory with temperature sensors (f7,b9,f0)  
base_dir = '/sys/bus/w1/devices/'
#f7 directory
device_folder_1 = glob.glob(base_dir + '28-030167944df7')[0]
device_file_1 = device_folder_1 + '/w1_slave'
#b9 directory
device_folder_2 = glob.glob(base_dir + '28-030797940')[0]
device_file_2 = device_folder_2 + '/w1_slave'
#f0 directory
device_folder_3 = glob.glob(base_dir + '28-03219779f01')[0]
device_file_3 = device_folder_3 + '/w1_slave'

# Setup ADC Sensor
i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads,ADS.P1)

# Setup Pubber
pubber = Publisher(client_id="jet-pubber")

def read_temp_raw():
	f = open(device_file_1, 'r')
	temp1 = f.readlines()
	f.close()
	f = open(device_file_2, 'r')
	temp2 = f.readlines()
	f.close()
	f = open(device_file_3, 'r')
	temp3 = f.readlines()
	f.close()
	print(temp1 + " : " + temp2 + " : "+temp3 + ":" )
	return temp1
 
def read_temp():
	temp1 = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		temo1 = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

def publish_temp_status():
	temp_c, temp_f = read_temp()
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
	publish_temp_status()
	publish_adc_status()
	time.sleep(1)

