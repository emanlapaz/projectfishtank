#release 1: get the sensehat sensors and joystick working

from sense_hat import SenseHat
from datetime import datetime
import random, time
from random import randint
import sys

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
   sense_gyro = sense.get_gyroscope()
   gyroscope = round(sense_gyro, 2)
   sense_accel = sense.get_accelerometer()
   accelerometer = round (sense_accel, 2)

#prints the value in the console with 2 seconds delay
   print("Temperature: %s C" % temperature)
   time.sleep(2)
   print("Humidity: %s %%" % humidity)
   time.sleep(2)
   print("Pressure: %s Millibars" % pressure)
   time.sleep(2)
   print("Gyroscope p: {pitch}, r: {roll}, y: {yaw}".format(**gyroscope))
   time.sleep(2)
   print("Accelerometer p: {pitch}, r: {roll}, y: {yaw}".format(**accelerometer))



while True:
    sensor_readings()

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
            sense.show_letter("M")