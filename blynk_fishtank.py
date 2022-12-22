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
import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import os
import storeFileFB
from BlynkTimer import BlynkTimer

from threading import Thread
from threading import Event
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

BLYNK_AUTH = 'D_mFZtGQutqMZJFeSFj9MDUb7IknvwqN'
blynk = BlynkLib.Blynk(BLYNK_AUTH) 
timer = BlynkTimer()
bucket = storage.bucket()
now = datetime.now()
sense = SenseHat()
camera = PiCamera()
frame = 1
global value
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

#Water Status
@blynk.on("V10")
def water_status():
    water_temp = tank_temp()
    if water_temp <= 24:
        blynk.log_event("tank_temp_low")
        return 0
    elif water_temp >= 28:
        blynk.log_event("tank_temp_high")
        return 2
    else:
        return 1


#Room Status
@blynk.on("V13")
def room_status():
    
    room_temp = ambient_temp()
    if room_temp <= 18:
        blynk.log_event("room_temp_low")
        return 0
    elif room_temp >= 24:
        blynk.log_event("room_temp_high")
        return 2
    else:
        return 1


#Alarm Triggered
@blynk.on("V9")
def alarm_triggered():
    orientation = sense.get_orientation_degrees()
    pitchOrient = orientation['pitch']
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
    #if pitchOrient <=90 and pitchOrient >30:
    if pitchOrient <350 and pitchOrient >=10:
        blynk.log_event("lid_moved")
        return 1
    else:
        return 0

@blynk.on("V0")
def lightSwitch(value):
    blynk.virtual_write(0)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    buttonValue=value[0]
    if buttonValue == "1":
        print(f'Light On at {dt_string}')
        sense.clear( 255, 0, 0 )
        sense.clear( 0, 255, 0 )
    elif buttonValue == "0":
        print(f'Light Off at {dt_string}')
        sense.clear()


feed_timer = 5
def feed_countdown(feed_timer):
    blynk.virtual_write(5, "Alarm Deactivated: Feed Now")
    while feed_timer:
        mins, secs = divmod(feed_timer, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        feed_timer -= 1
    

@blynk.on("V3")
def feedSwitch(value):
    blynk.virtual_write(3)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    buttonValue=value[0]
    if buttonValue == "1":
        sense.clear( 0, 255, 0 )
        time.sleep(1)
        feed_countdown(feed_timer)
        if buttonValue == "1":
            blynk.virtual_write(3, 0)
            sense.clear( 255, 0, 0 )
            blynk.virtual_write(5, "Alarm Activated: Dont Feed")
        return 1

    elif buttonValue == "0":
        sense.clear()
        return 0

clean_timer= 10
def clean_countdown(clean_timer):
    blynk.virtual_write(8, "Alarm Deactivated: Clean Now")
    while clean_timer:
        mins, secs = divmod(clean_timer, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        clean_timer -= 1
    print("Alarm Activated!")

@blynk.on("V4")
def clean_Switch(value):
    blynk.virtual_write(4)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    buttonValue=value[0]
    if buttonValue == "1":
        sense.clear( 255, 0, 0 )
        time.sleep(3)
        sense.clear( 0, 255, 0 )
        time.sleep(3)
        sense.show_message("Clean Now!", text_colour = green)
        clean_countdown(clean_timer)
        if buttonValue == "1":
            blynk.virtual_write(4, 0)
            sense.clear( 255, 0, 0 )
            blynk.virtual_write(8, "Alarm Activated: Dont Clean")
        return 1
        
    elif buttonValue == "0":
        sense.clear()
        return 0

@blynk.on("V11")
def triggered_date():
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    if alarm_triggered() == 1:
        return dtString
    elif alarm_triggered() == 0:
        pass

def cameraCapture():
    fileLoc = f'/home/pi/fishtank/images/frame{frame}.jpg' # set the location of image file and current time
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    camera.capture(fileLoc) # capture image and store in fileLoc
    print("lid was moved- photo taken")
    print(f'frame {frame} taken at {dt_string}') # print frame number to console
    storeFileFB.store_file(fileLoc)
    storeFileFB.push_db(fileLoc, dt_string)
    print('Image stored and location pushed to db')
    sense.clear( 0, 0, 255 )
    time.sleep ( 0.33 )
    sense.clear( 255, 0, 0 )
    sense.clear( 0, 0, 255 )
    time.sleep ( 0.33 )
    sense.clear( 255, 0, 0 )

#timers
timer.set_interval(30, tank_temp)
timer.set_interval(30, ambient_temp)
timer.set_interval(30, water_status)
timer.set_interval(30, room_status)

while True:
    blynk.run()
    timer.run()
    blynk.virtual_write(1, tank_temp())
    blynk.virtual_write(2, ambient_temp())
    blynk.virtual_write(10, water_status())
    blynk.virtual_write(13, room_status())
    blynk.virtual_write(9, alarm_triggered())
    blynk.virtual_write(11, triggered_date())

    if alarm_triggered() == 1:
        cameraCapture()
        frame += 1
    elif alarm_triggered() == 0:
        sense.clear()
          
            
                
                


