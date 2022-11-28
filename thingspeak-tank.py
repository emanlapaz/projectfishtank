#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
from sense_hat import SenseHat
import logging
from dotenv import dotenv_values
from datetime import datetime
from time import sleep
from random import randint
import random, time
import os
import glob
from picamera import PiCamera
import datetime


#Initialise SenseHAT
sense = SenseHat()
sense.clear()

#load MQTT configuration values from .env file
config = dotenv_values(".env")

#configure Logging
logging.basicConfig(level=logging.INFO)

# Define event callbacks for MQTT
def on_connect(client, userdata, flags, rc):
    logging.info("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    logging.info("Message Sent ID: " + str(mid))

mqttc = mqtt.Client(client_id=config["clientId"])

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# parse mqtt url for connection details
url_str = sys.argv[1]
print(url_str)
url = urlparse(url_str)
base_topic = url.path[1:]

# Configure MQTT client with user name and password
mqttc.username_pw_set(config["username"], config["password"])

#Connect to MQTT Broker
mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

#Set Thingspeak Channel to publish to
topic = "channels/"+config["channelId"]+"/publish"

def room_temp():
        temp=round(sense.get_temperature(),2)
        payload="field1="+str(temp)
        mqttc.publish(topic, payload)
        time.sleep(int(config["transmissionInterval"]))
        print("Temperature: %s C" % temp)

def water_temp(): 
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
 
        def read_temp_raw():
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines
 
        def read_temp():
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
            lines = read_temp_raw()

            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
        
        #temp=round(sense.get_temperature(),2)
        payload="field2="+str(water_temp())
        mqttc.publish(topic, payload)
        time.sleep(int(config["transmissionInterval"]))

        print("Water Temperature: %s C" % water_temp())

# Publish a message to temp every 15 seconds
while True:
    try:
        room_temp()
        water_temp()
    except:
        logging.info('Interrupted')