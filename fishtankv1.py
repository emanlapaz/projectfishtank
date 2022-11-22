#release 1: get the sensehat sensors and joystick working

from sense_hat import SenseHat
from datetime import datetime
from gpiozero import LED
from time import sleep
from random import randint
import random, time
import sys
import os
import glob
import time

#initial senseHat set up
sense = SenseHat()
sense.clear()

#senseHat LED colours
blue = (0,0,255)
yellow = (255,255,0) 
red = (255,0,0)
black = (0,0,0)
grey = (55,55,55)
white = (255,255,255)
green = (0,255,0)
magenta = (255,0,255)
cyan = (0,255,255)

#FUNCTIONS

#sensor readings

def sensor_readings():
   global temperature
   global pressure
   global humidity
   global gyroscope
   global accelerometer

#temperature sensor
   sense_temp = sense.get_temperature()
   temperature = round(sense_temp, 2)

#pressure sensor
   sense_pressure = sense.get_pressure()
   pressure = round(sense_pressure, 2)

#humidity snesor
   sense_humid = sense.get_humidity()
   humidity = round(sense_humid, 2)

# gyroscope and accelerometer
   sense.set_imu_config(False, True, True)
   gyroscope = sense.get_gyroscope()
   accelerometer= sense.get_accelerometer()


#prints the value in the console with 2 seconds delay
   print("Temperature: %s C" % temperature)
   print("Humidity: %s %%" % humidity)
   print("Pressure: %s Millibars" % pressure)
   print("Gyroscope p: {pitch}, r: {roll}, y: {yaw}".format(**gyroscope))
   print("Accelerometer p: {pitch}, r: {roll}, y: {yaw}".format(**accelerometer))

def lid_moved():
    if gyroscope != 0:
        print("lid moved")

def was_moved():
        accel = sense.get_accelerometer_raw()
        x = accel['x']
        y = accel['y']
        z = accel['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if x > 1 or y > 1 or z > 1:
            print("lid was moved")
        else:
            sense.clear

"""def blink():
        red = LED(18)
        red.on()
        sleep(1)
        red.off()
        sleep(1)
 """
# water temperature function: returns celcius---- remove farhenheit reading
# reference: https://pimylifeup.com/raspberry-pi-temperature-sensor/
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
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c #, temp_f
        #print(read_temp())
        print("Water Temperature: %s C" % read_temp())
        #while True:
	       
	       #time.sleep(1)

                
while True:
    sensor_readings()
    time.sleep(1)
    water_temp()
    time.sleep(1)
    for x in sense.stick.get_events():
        if x.direction == 'up':
            sense.show_message("T: %s C" % temperature)
        elif x.direction == 'down':
            sense.show_message("H: %s " % humidity)
        elif x.direction == 'left':
            sense.show_message("P: %s mmHg" % pressure)
        elif x.direction == 'right':
            sense.show_message("Hi")
        elif x.direction == 'middle':
            sense.clear
    #lid_moved()
    was_moved()
    #blink()
    sense.clear

    