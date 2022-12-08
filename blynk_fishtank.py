#Project FishTank
#Eugenio Manlapaz
# This is a Blynk IOT project using Python
import BlynkLib
import os
import glob
import time
from sense_hat import SenseHat
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

BLYNK_AUTH = 'D_mFZtGQutqMZJFeSFj9MDUb7IknvwqN'
blynk = BlynkLib.Blynk(BLYNK_AUTH) 

sense = SenseHat()
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

@blynk.on("V0")
def v0_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    if buttonValue =="1":
        sense.show_message("ARMED!", text_colour = red)
    elif buttonValue =="0":
        sense.show_message("DISARMED!", text_colour = green)

@blynk.on("V1")
def v1_write_handler():

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
        
@blynk.on("V2")
def v2_write_handler():

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

@blynk.on("V10")
def v10_write_handler():
    #water_status = v1_write_handler()
    if v1_write_handler() <= 24:
        return 0
    elif v1_write_handler() >= 28:
        return 2
    else:
        return 1

while True:
        blynk.run()
        time.sleep(.5)
        blynk.virtual_write(1, v1_write_handler())
        blynk.virtual_write(2, v2_write_handler())
        blynk.virtual_write(10, v10_write_handler())