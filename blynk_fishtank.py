#libraries
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

#set up for the termperature probe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Blynk authorisation token
BLYNK_AUTH = 'D_mFZtGQutqMZJFeSFj9MDUb7IknvwqN'

#initilise
blynk = BlynkLib.Blynk(BLYNK_AUTH) 
timer = BlynkTimer()
bucket = storage.bucket()
now = datetime.now()
sense = SenseHat()
camera = PiCamera()
frame = 1
camera.start_preview()
sense.set_imu_config(False, True, False) #gyroscope only
sense.clear()# resets the SenseHat

#colours
R = (255, 0, 0) #red
B = (0,0,255) #blue
G = (0,255,0) #green
O = (255,127,0) #orange
W = (0, 0, 0) #Black

red_face = [
     W, W, R, R, R, R, W, W,
     W, R, W, W, W, W, R, W,
     R, W, R, W, W, R, W, R,
     R, W, W, W, W, W, W, R,
     R, W, W, R, R, W, W, R,
     R, W, R, W, W, R, W, R,
     W, R, W, W, W, W, R, W,
     W, W, R, R, R, R, W, W
]

green_face = [
     W, W, G, G, G, G, W, W,
     W, G, W, W, W, W, G, W,
     G, W, G, W, W, G, W, G,
     G, W, W, W, W, W, W, G,
     G, W, G, W, W, G, W, G,
     G, W, W, G, G, W, W, G,
     W, G, W, W, W, W, G, W,
     W, W, G, G, G, G, W, W
]

orange_face = [
     W, W, O, O, O, O, W, W,
     W, O, W, W, W, W, O, W,
     O, W, O, W, W, O, W, O,
     O, W, W, W, W, W, W, O,
     O, W, O, W, W, O, W, O,
     O, W, W, O, O, W, W, O,
     W, O, W, W, W, W, O, W,
     W, W, O, O, O, O, W, W
]

#Ds18B20 set up
global base_dir
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28*')[1]
device_file = device_folder + '/w1_slave'
device_file1 = device_folder1 + '/w1_slave'

#Water Temperature - returns value in Celcius
@blynk.on("V1") #Virtual pin 1 on blynk datastream
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

        return water_temp()

#Room Temperature returns Celcius value
@blynk.on("V2") #Virtual pin 2 on blynk datastream
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

        return room_temp()

#Water Status - enumerable data type on Blynk- triggers Blynk events
@blynk.on("V10") #Virtual pin 10 on blynk datastream
def water_status():
    water_temp = tank_temp()
    if water_temp <= 24:
        blynk.log_event("tank_temp_low")
        return 0 #displays "water too cold" on label widget
    elif water_temp >= 28:
        blynk.log_event("tank_temp_high")
        return 2 #displays "water too warm" on label widget
    else:
        return 1 #displays "water temp normal" on label widget


#Room Status- enumerable data type on Blynk- triggers Blynk events
@blynk.on("V13") #Virtual pin 13 on blynk datastream
def room_status():
    room_temp = ambient_temp()
    if room_temp <= 18:
        blynk.log_event("room_temp_low")
        return 0 #displays "room too cold" on label widget
    elif room_temp >= 24:
        blynk.log_event("room_temp_high")
        return 2 #displays "room too warm" on label widget
    else:
        return 1 #displays "room temp normal" on label widget


#Alarm Triggered- main alarm function. If triggered, will activate alarm lights, start camera capture, and Blynk notifications
@blynk.on("V9") #Virtual pin 9 on blynk datastream
def alarm_triggered():
    orientation = sense.get_orientation_degrees() #uses gyroscope sensor to detect changes in angle
    pitchOrient = orientation['pitch']# uses pitch
    print("p: {pitch}".format(**orientation))
    #if pitchOrient <=90 and pitchOrient >30: #narrower angle detection scope
    if pitchOrient <350 and pitchOrient >=10: #wider angle detection scope used for trials
        blynk.log_event("lid_moved") # critical event. notifies user if the lid was moved
        return 1 #shows a bar on blynk charts with the date/time stamp
    else:
        return 0

@blynk.on("V0") #Virtual pin 0 on blynk datastream
def lightSwitch(value): #utility light function
    blynk.virtual_write(0) #writes to virtual pin 0
    buttonValue=value[0]
    if buttonValue == "1":
        sense.clear( 255, 255, 255 ) #lights up the sensehat LED matrix
    elif buttonValue == "0":
        sense.clear()


feed_timer =10 # user input, can be changed as needed, used the countdown timer to hold the gyroscope readings thus preventing alarms
def feed_countdown(feed_timer):
    blynk.virtual_write(5, "Feed Now") #writes on virtual pin 5 and diplays the "Feed Now" on the Blynk dash
    while feed_timer:
        mins, secs = divmod(feed_timer, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        feed_timer -= 1
    

@blynk.on("V3") #Virtual pin 3 on blynk datastream
def feedSwitch(value): #feed switch function
    blynk.virtual_write(3) #writes on virtual pin 3 and diplays the "Feed Now" on the Blynk dash
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") #date/time stamp
    buttonValue=value[0]
    if buttonValue == "1":
        sense.show_message("Feed Now!", text_colour = O) #shows message on sensehat LED matrix
        sense.set_pixels(orange_face)   #displays and orange smiley on the LED matrix
        time.sleep(1)
        feed_countdown(feed_timer) #starts the countdown
        if buttonValue == "1": #checks the button value
            blynk.virtual_write(3, 0) #changes the buttonstate from 1 to 0, turns off feed switch
            sense.show_message("ALARM ON!", text_colour = R) #shows message on sensehat LED matrix
            sense.set_pixels(red_face) #displays and red sad smiley on the LED matrix
            blynk.virtual_write(5, "Alarm Activated: Dont Feed") #writes on virtual pin 5, lets the user know that alarm is back on
        return 1

    elif buttonValue == "0":
        sense.clear() # clears the sensehat
        return 0

clean_timer= 10 # user input, can be changed as needed, used the countdown timer to hold the gyroscope readings thus preventing alarms
def clean_countdown(clean_timer):
    blynk.virtual_write(8, "Clean Now!")
    while clean_timer: 
        mins, secs = divmod(clean_timer, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        timeformat = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        clean_timer -= 1

@blynk.on("V4") #Virtual pin 4 on blynk datastream
def clean_Switch(value): #writes on virtual pin 3 and diplays the "Clean Now" on the Blynk dash
    blynk.virtual_write(4)
    buttonValue=value[0]
    if buttonValue == "1":
        sense.show_message("Clean Now!", text_colour = G) #displays message on sensehat LED matrix
        sense.set_pixels(green_face) #green smiley on sensehat LED
        clean_countdown(clean_timer) #starts the countown timer
        if buttonValue == "1": #checks button state
            blynk.virtual_write(4, 0) #writes on virtual pin 4 and changes 1 to 0
            sense.show_message("ALARM ON!", text_colour = R) #displays alarm status
            sense.set_pixels(red_face) #red sad face on sensehat lED matrix
            blynk.virtual_write(8, "Alarm Activated: Dont Clean") #writes on virtual pin 8 and diplays string on Blynk dashboard
        return 1
        
    elif buttonValue == "0":
        sense.clear() #clears the sensehat
        return 0

@blynk.on("V11") #Virtual pin 11 on blynk datastream
def triggered_date(): #returns a date/time stamp of the recent alarm triggered and dispalys on Blynk dash
    dtString = now.strftime("%d/%m/%Y %H:%M:%S") #current date/time
    if alarm_triggered() == 1:
        return dtString
    elif alarm_triggered() == 0:
        pass

def cameraCapture(): #Picamera image capture
    fileLoc = f'/home/pi/fishtank/images/frame{frame}.jpg' # set the location of image file and current time
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") #date/time stamp
    camera.capture(fileLoc) # capture image and store in fileLoc
    print("lid was moved- photo taken")
    print(f'frame {frame} taken at {dt_string}') # print frame number to console
    storeFileFB.store_file(fileLoc) #stores to Firebase
    storeFileFB.push_db(fileLoc, dt_string)
    print('Image stored and location pushed to db')
    sense.clear( 0, 0, 255 ) #light up the Sensehat LED matrix with the alarm light ( blinking red/blue)
    time.sleep ( 0.33 )
    sense.clear( 255, 0, 0 )
    sense.clear( 0, 0, 255 )
    time.sleep ( 0.33 )
    sense.clear( 255, 0, 0 )

#timers- returs the values on 30 second intervals
timer.set_interval(30, tank_temp)
timer.set_interval(30, ambient_temp)
timer.set_interval(30, water_status)
timer.set_interval(30, room_status)

while True:
    blynk.run() #main blynk fuctions- waits for events
    blynk.virtual_write(1, tank_temp())
    blynk.virtual_write(2, ambient_temp())
    blynk.virtual_write(10, water_status())
    blynk.virtual_write(13, room_status())
    blynk.virtual_write(9, alarm_triggered())
    blynk.virtual_write(11, triggered_date())

    #main alarm loop. will take an image as long as the sensehat is not on a level surface
    if alarm_triggered() == 1:
        cameraCapture() #camera function
        frame += 1
    elif alarm_triggered() == 0:
        sense.clear()
          
            
                
                


