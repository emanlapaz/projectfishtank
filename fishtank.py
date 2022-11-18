from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

#temperature
temp = sense.get_temperature()
print("Temperature: %s C" % temp)

#humidity
humidity = sense.get_humidity()
print("Humidity: %s %%" % humidity)

#pressure
pressure = sense.get_pressure()
print("Pressure: %s Millibars" % pressure)

#gyroscope
sense.set_imu_config(False, True, False)  # gyroscope only
gyro_only = sense.get_gyroscope()
print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))

#accelerometer
sense.set_imu_config(False, False, True)  # accelerometer only
accel_only = sense.get_accelerometer()
print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))

sense = SenseHat()
event = sense.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))
sleep(0.1)
event = sense.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))

from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

#set your colors here
background = (198, 30, 74)
color = (255, 255, 255)

#display a message on the screen
sense.show_message("RaspberryTips <3", 0.05, color, background)
sleep(1)

#display only one letter
sense.show_letter("@")
sleep(2)

#turn off the screen
sense.clear()

R = (198, 30, 74)       #raspberrytips red
W = (255, 255, 255)     #white

#set all pixels at once
pixels = [
     W, W, W, W, W, W, W, W,
     W, R, R, W, R, R, W, W,
     R, R, R, R, R, R, R, W,
     R, R, R, R, R, R, R, W,
     R, R, R, R, R, R, R, W,
     W, R, R, R, R, R, W, W,
     W, W, R, R, R, W, W, W,
     W, W, W, R, W, W, W, W
]

sense.set_pixels(pixels)
sleep(5)
sense.clear()

#set one pixel at at time
while True:
        X = randint(0, 7)
        Y = randint(0, 7)
        sense.set_pixel(X, Y, R)
        sleep(0.2)

"""

EMOTICON CLEANING
     HAPPY FACE GREEN
     W, W, G, G, G, G, W, W,
     W, G, W, W, W, W, G, W,
     G, W, G, W, W, G, W, G,
     G, W, W, W, W, W, W, G,
     G, W, G, W, W, G, W, G,
     G, W, W, G, G, W, W, G,
     W, G, W, W, W, W, G, W,
     W, W, G, G, G, G, W, W

     SAD FACE RED
     W, W, R, R, R, R, W, W,
     W, R, W, W, W, W, R, W,
     R, W, R, W, W, R, W, R,
     R, W, W, W, W, W, W, R,
     R, W, W, R, R, W, W, R,
     R, W, R, W, W, R, W, R,
     W, R, W, W, W, W, R, W,
     W, W, R, R, R, R, W, W

     MHE FACE ORANGE
     W, W, O, O, O, O, W, W,
     W, O, W, W, W, W, O, W,
     O, W, O, W, W, O, W, O,
     O, W, W, W, W, W, W, O,
     O, W, W, W, W, W, W, O,
     O, W, O, O, O, O, W, O,
     W, O, W, W, W, W, O, W,
     W, W, O, O, O, O, W, W,

     EMOTICON FEED
    GOOD GREEN
     W, W, W, W, W, W, W, W,
     G, G, G, W, W, W, W, W,
     G, W, G, W, W, W, W, G,
     G, W, G, W, W, W, G, W,
     G, W, G, W, W, G, W, W,
     G, W, G, W, G, W, W, W,
     G, G, G, W, W, W, W, W,
     W, W, W, W, W, W, W, W,

    DUE ORANGE
     W, W, W, W, W, W, W, W,
     O, O, O, W, W, W, W, W,
     O, W, O, W, W, W, W, W,
     O, W, O, W, O, O, O, O,
     O, W, O, W, W, W, W, W,
     O, W, O, W, O, O, O, O,
     O, O, O, W, W, W, W, W,
     W, W, W, W, W, W, W, W,

    OVERDUE RED
     W, W, W, W, W, W, W, W,
     R, R, R, W, W, W, W, W,
     R, W, R, W, R, W, W, R,
     R, W, R, W, W, R, R, W,
     R, W, R, W, W, R, R, W,
     R, W, R, W, R, W, W, R,
     R, R, R, W, W, W, W, W,
     W, W, W, W, W, W, W, W,
"""

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause

x = 3
y = 3
sense = SenseHat()

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y - 1)

def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y + 1)

def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x - 1)

def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x + 1)

def refresh():
    sense.clear()
    sense.set_pixel(x, y, 255, 255, 255)

sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_any = refresh
refresh()
pause()