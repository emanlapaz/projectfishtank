# projectfishtank image
# edit and finalize

![RiAB9Xk6T](https://user-images.githubusercontent.com/96552779/208731692-a823ca14-21fd-4e9c-94e2-146962f121f7.jpg)
Project fishtank



Student Name: Eugenio Manlapaz
Student ID: 20100013
Project Repo: https://github.com/emanlapaz/projectfishtank
Glitch URL: https://angry-uttermost-gaura.glitch.me/
Youtube Video Link: 

Introduction:
	Project fishtank is an IOT project using the Raspberry pi. Tropical aquarium fish needs a certain temperature range to be healthy and reproduce. Proper cycling of light and water is also very essential same as with the feeding schedule. The aim of this project is to use the Raspberry Pi to monitor activities such as feeding and cleaning, temperature (ambient and water temperature), and any unwanted events that could happen ( e.g. a toddler opening the lid and pouring all the feed inside the tank).
 
Materials:
1.	Raspberry pi
2.	Sense Hat
a.	Sense Hat LED matrix for displays
b.	Temperature sensor for ambient room temperature (D18B20)
c.	Gyroscope to detect movement (lid opening)
d.	Sensehat Joystick
3.	PiCamera
4.	Waterproof temperature probe (submerged in tank) D18B20 with breakout board
5.	Break out board
6.	40 pin extension Header


Tech:
1.	Wi-Fi
2.	Blynk for buttons and charts
3.	Blynk for Mobile app connection
4.	FireBase
5.	Glitch
6.	Visual Code for SSH and Code editor
7.	Python for programming language

Functions:
1. Water temperature (Fish Tank Temp)
2. Ambient temperature (Room Temp)
3. Feed Timer
4. Cleaning Timer
5. Movement Detection using SenseHat Gyroscope

Applications:
1.	Monitors water temperature and room temperature.
2.	Monitor feeding status via Blynk charts and Timers
	#Sends notifications when feeding due or over due (Lights green rectangle when feed still okay, orange when 1 day passed, red when >3 days past)
3. 	Monitor cleaning status
	#sends notifications when cleaning due, over due (Lights green smiley 😉, orange when 1 day passed 😐, red sad face when >3 days passed ☹)
4.	Motion Detection: Checks if lid is open/moved using the senseHat Gyroscope Pitch
5.	Security alarm: If lid moved, captures an image and sends it to Firebase DB. Most Recent image can be viewed in the Glitch URL:
6.	#live streaming via Blink video
7.	SenseHat LED matrix as light source

Raspberry Pi Set Up:

I am using a Raspberry Pi 4B 2gb with a 40 pin header extension to attach the SenseHat and the D18B20 temperature sensor. 
#RPi
#2 way 40 pin header extension. The 2 way header extension enables me to attach the SenseHat and use the Pins for other attachments. I used a breakout board and connected 2 D18B20 sensors(parallel connection). The One Wire ### allows parallel connections with multiple D18B20 sensors. Pins used are the 3V, ##, ##
#D18B20 temperature sensor



REFERENCES:
