#release 1 v4: get the sensehat sensors and joystick working, photo when moved, added timers

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
from picamera import PiCamera
import datetime

#initial senseHat set up
sense = SenseHat()
sense.clear()
camera = PiCamera()


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


#prints the value in the console
   print("Temperature: %s C" % temperature)
   #print("Humidity: %s %%" % humidity)
   #print("Pressure: %s Millibars" % pressure)
   #print("Gyroscope p: {pitch}, r: {roll}, y: {yaw}".format(**gyroscope))
   #print("Accelerometer p: {pitch}, r: {roll}, y: {yaw}".format(**accelerometer))

# captures a photo when lid is moved- can only take one photo and Overwrites
def lid_moved():
        camera.start_preview()
        frame = 1
        accel = sense.get_accelerometer_raw()
        x = accel['x']
        y = accel['y']
        z = accel['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if x > 1 or y > 1 or z > 1:
            fileLoc = f'/home/pi/fishtank/images/frame{frame}.jpg' # set the location of image file and current time
            currentTime = datetime.datetime.now().strftime("%H:%M:%S")
            camera.capture(fileLoc) # capture image and store in fileLoc
            print("lid was moved- photo taken")
            print(f'frame {frame} taken at {currentTime}') # print frame number to console
            frame += 1

        else:
            sense.clear


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
            return temp_c

        print("Water Temperature: %s C" % read_temp())

                
while True:
    sensor_readings()
    water_temp()
    lid_moved()
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
    sense.clear

    
"""
# timer function for the feed.
#
import time
#from sense_hat import SenseHat
#import threading

def countdown(timer):
    print("starting countdown")
    while timer:
        mins, secs = divmod(timer, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        timer -= 1
    print("feed due now!")
    

def feed_due(time_overdue):
    while time_overdue <=6:
        mins, secs = divmod(time_overdue, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_overdue += 1
        
    print("feed overdue 6 hours GREEN")
   

    while time_overdue <=12:
        mins, secs = divmod(time_overdue, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_overdue += 1
    print("feed overdue 12 hours ORANGE")

    while time_overdue <=24:
        mins, secs = divmod(time_overdue, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_overdue += 1
    print("feed overdue 24 hours RED")
    
while True:
    #24 hrs-countdown(86400)
    #12  43200
    #6 21600
    
    countdown(3)
    for x in sense.stick.get_events():
        if x.direction == 'middle':
            countdown(3)
        else:
            feed_due(1)
    
    #feed_dueOrange(6)
    #feed_dueRed(12)

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
            pass
    break
    
"""

