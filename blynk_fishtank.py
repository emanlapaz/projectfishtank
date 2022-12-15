#work on ALARM, FEED, CLEAN
#work on camera

import BlynkLib
import os
import glob
import time
import threading
import datetime
from sense_hat import SenseHat
from datetime import datetime
from picamera import PiCamera

from threading import Thread
from threading import Event
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

BLYNK_AUTH = 'D_mFZtGQutqMZJFeSFj9MDUb7IknvwqN'
blynk = BlynkLib.Blynk(BLYNK_AUTH) 

now = datetime.now()
sense = SenseHat()
camera = PiCamera()
frame = 1
camera.start_preview()
sense.set_imu_config(True, True, True)
sense.clear()


red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)



global base_dir
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28*')[1]
device_file = device_folder + '/w1_slave'
device_file1 = device_folder1 + '/w1_slave'


#Water Temperature
@blynk.on("V1")
def tank_temp():

        def read_rom():
            name_file = device_folder+'/name'
            f = open(name_file,'r')
            #print('f:',f)
            return f.readline()
 
        def read_temp_raw():
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines

        def water_temp():
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
            lines = read_temp_raw()

            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

        return water_temp()

#Room Temperature       
@blynk.on("V2")
def ambient_temp():

        def read_rom1():
            name_file1 = device_folder1+'/name'
            g = open(name_file1,'r')
            #print('g:',g)
            return g.readline()

        def read_temp_raw1():
            g = open(device_file1, 'r')
            lines1 = g.readlines()
            #print('raw_g',lines1)
            g.close()
            return lines1

        def room_temp():
            lines1 = read_temp_raw1()
            while lines1[1].strip()[-3:] != 'YES':
                lines1 = read_temp_raw1()
                equals_pos1 = lines1[1].find('t=')
                temp_string1 = lines1[1][equals_pos1 +2:]
                temp_c1 = float(temp_string1) / 1000.0
                return temp_c1

        return room_temp()

#Alarm Triggered
@blynk.on("V9")
def alarm_triggered():
    orientation = sense.get_orientation_degrees()
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

    if orientation['pitch'] <=180 and orientation ['pitch'] >=90:
        #print("Alarm activated")
        return 1
    else:
        return 0

@blynk.on("V0")
def alarm_button(value):
    buttonValue=value[0]
    print(f'Alarm Switch: {buttonValue}')
    if buttonValue =="1":
        #sense.show_message("ARMED!", text_colour = red)
        print("1")
    elif buttonValue =="0":
        print("0")
        #sense.show_message("DISARMED!", text_colour = green)
        
#Water Status
@blynk.on("V10")
def water_status():
        water_temp = tank_temp()
        if water_temp <= 24:
            return 0
        elif water_temp >= 28:
            return 2
        else:
            return 1

@blynk.on("V11")
def triggered_date():
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if alarm_triggered() == 1:
            return  dt_string

while True:
        blynk.run()
        blynk.virtual_write(1, tank_temp())
        blynk.virtual_write(2, ambient_temp())
        blynk.virtual_write(10, water_status())
        blynk.virtual_write(9, alarm_triggered())
        blynk.virtual_write(11, triggered_date())

        if alarm_triggered():
            fileLoc = f'/home/pi/fishtank/images/frame{frame}.jpg' # set the location of image file and current time
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            camera.capture(fileLoc) # capture image and store in fileLoc
            print("lid was moved- photo taken")
            print(f'frame {frame} taken at {dt_string}') # print frame number to console
            frame += 1

