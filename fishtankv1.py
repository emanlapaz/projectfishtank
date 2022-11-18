from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

#temperature
temp = sense.get_temperature()
print("Temperature: %s C" % temp)