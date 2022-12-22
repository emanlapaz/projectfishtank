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

#one wire interface for the DS18b20 sensor 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Blynk Authentication
BLYNK_AUTH = 'D_mFZtGQutqMZJFeSFj9MDUb7IknvwqN'
blynk = BlynkLib.Blynk(BLYNK_AUTH) 

#initialize
bucket = storage.bucket()
now = datetime.now()
sense = SenseHat()
camera = PiCamera()
frame = 1
timer = BlynkTimer()

camera.start_preview()# PiCamera
sense.set_imu_config(True, True, True) #sets the gyroscope, magnetometer and acceloremeter on
sense.clear() #clears the Rpi

#colours
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)


#set up for the temperature sensors
global base_dir
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28*')[1]
device_file = device_folder + '/w1_slave'
device_file1 = device_folder1 + '/w1_slave'

#Water Temperature (FishTank) measurement using the DS18B20 temperature sensor
@blynk.on("V1")# water temp sensor set a virtual pin 1
def tank_temp():

        def read_rom():
            name_file = device_folder+'/name'
            f = open(name_file,'r')
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

        return water_temp()#returns temperature in Celcius

#Room Temperature measurement using the DS18B20 temperature sensor
@blynk.on("V2")## room temperature set at virtual pin 2
def ambient_temp():

        def read_rom1():
            name_file1 = device_folder1+'/name'
            g = open(name_file1,'r')
            return g.readline()

        def read_temp_raw1():
            g = open(device_file1, 'r')
            lines1 = g.readlines()
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

        return room_temp() #returns temperature in Celcius

#Water Status - triggers Blynk events. Critical event for Tank temp low.
@blynk.on("V10")# set up with virtual pin 10 - enumerable.
def water_status():
    water_temp = tank_temp()
    if water_temp <= 24:
        blynk.log_event("tank_temp_low")
        return 0 # displays water temp low" on Blynk dashboard
    elif water_temp >= 28:
        blynk.log_event("tank_temp_high")
        return 2 # displays "water temp high" on Blynk dashboard
    else:
        return 1# displays "water temp normal" on Blynk dashboard


#Room Status- triggers Blynk events
@blynk.on("V13")# set up with virtual pin 13- enumerable.
def room_status():
    room_temp = ambient_temp()
    if room_temp <= 18: 
        blynk.log_event("room_temp_low")
        return 0 #displays room temp low" on Blynk dashboard
    elif room_temp >= 24:
        blynk.log_event("room_temp_high")
        return 2 #displays room temp high" on Blynk dashboard
    else:
        return 1 #displays room temp normal" on Blynk dashboard

    

#Alarm Function- uses the Sensehat Gyroscope pitch readings to detect movement. Activates when pitch is in between 30 to 90 degrees
#This function needs multiple raeadings to be accurate. Using time.sleep to slow down the values will cause inaccurate/ weird values.
@blynk.on("V9")
def alarm_triggered():
    orientation = sense.get_orientation_degrees()
    pitchOrient = orientation['pitch'] # returns gyroscope pitch in degrees 
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation)) #prints pitch, roll, and yaw in terminal
    if pitchOrient <=90 and pitchOrient >30: # angle of movement that would be detected
        blynk.log_event("lid_moved") # triggers a Blynk Critical Event
        return 1
    else:
        return 0

#light switch- lights up the SenseHat LED
@blynk.on("V0") #virtual pi 0
def lightSwitch(value):
    blynk.virtual_write(0)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") #returns current date and time(timestamp)
    buttonValue=value[0]
    if buttonValue == "1":
        print(f'Light On at {dt_string}')
        sense.clear( 255, 255, 255 ) # white LED matrix light
    elif buttonValue == "0":
        print(f'Light Off at {dt_string}')
        sense.clear()
        
 
#returns date and time whenever the alarm is triggered
@blynk.on("V11") #virtual pin 11 datastream
def triggered_date():
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    if alarm_triggered() == 1:
        return dtString
    #try to remove this and see
    #elif alarm_triggered() == 0:
     #   pass

#PiCamera function
def cameraCapture():
    fileLoc = f'/home/pi/fishtank/images/frame{frame}.jpg' # set the location of image file and current time
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    camera.capture(fileLoc) # capture image and store in fileLoc
    print(f'frame {frame} taken at {dt_string}') # print frame number to console
    storeFileFB.store_file(fileLoc) #firebaseDB location
    storeFileFB.push_db(fileLoc, dt_string)
    print('Image stored and location pushed to db')
    #lights up the LED Red/Blue (Warnin light)
    sense.clear( 0, 0, 255 )
    time.sleep ( 0.33 )
    sense.clear( 255, 0, 0 )
    sense.clear( 0, 0, 255 )
    time.sleep ( 0.33 )
    sense.clear( 255, 0, 0 )

#Blynk timers- returns readings to the BlynK Server at a 30 seconds interval
timer.set_interval(30, tank_temp)
timer.set_interval(30, ambient_temp)
timer.set_interval(30, water_status)
timer.set_interval(30, room_status)

while True:
    blynk.run()
    timer.run()
   #DataStreams
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
          
            
                
                


