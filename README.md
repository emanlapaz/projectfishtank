Project FishTank IOT

<img src="https://user-images.githubusercontent.com/96552779/208731692-a823ca14-21fd-4e9c-94e2-146962f121f7.jpg" width=50% height=50%>




Student Name: Eugenio Manlapaz

Student ID: 20100013

Project Repo: https://github.com/emanlapaz/projectfishtank

Glitch URL: https://angry-uttermost-gaura.glitch.me/

Youtube Video Link: 


INTRODUCTION:

Project fishtank is an IOT project using the Raspberry pi. Tropical aquarium fish needs a certain temperature range to be healthy and reproduce. Proper cycling of light and water is also very essential same as with the feeding schedule. The aim of this project is to use the Raspberry Pi to monitor activities such as feeding and cleaning, temperature (ambient and water temperature), and any unwanted events that could happen ( e.g. a toddler opening the lid and pouring all the feed inside the tank).
 
 
 <img src="https://user-images.githubusercontent.com/96552779/208762335-36238a13-1587-444e-b57f-d73847afb687.gif" width=50% height=50%>
 
 
MATERIALS:
1.	Raspberry pi
<img src="https://user-images.githubusercontent.com/96552779/208762854-578c98fb-3f9d-4e1a-86b8-6a0f2b37da93.jpg" width=50% height=50%>


2.	Sense Hat
<img src="https://user-images.githubusercontent.com/96552779/208763569-8e1ec9a2-470d-4b3c-b3f9-950846aa24c3.jpg" width=50% height=50%>

3.	PiCamera

<img src="https://user-images.githubusercontent.com/96552779/208762662-d984c1b1-69e3-4079-945c-5a3bd8dbda18.jpg" width=50% height=50%>

4.	D18B20 temperature sensors for the Fishtank and Room temperature

<img src="https://user-images.githubusercontent.com/96552779/208762940-be941b6c-eec2-46b9-b593-b5265a327d8b.jpg" width=50% height=50%>

5.	Break out Board

<img src="https://user-images.githubusercontent.com/96552779/208763005-a9d09615-5b97-4ba1-bb85-3b944c829385.jpg" width=50% height=50%>

6. 40 pin header extension
<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/extension.jpg" width=50% height=50%>

TECH USED:
1.	Wi-Fi

2.	Blynk for buttons and charts

3.	Blynk for Mobile app connection

4.	FireBase

5.	Glitch

6.	Visual Code for SSH and Code editor

7.	Python for programming language

FUNCTIONS:

1. Water temperature (Fish Tank Temp)

2. Ambient temperature (Room Temp)

3. Feed Monitor/ Logger

4. Cleaning Monitor/ Logger

5. Movement Detection using SenseHat Gyroscope

Applications:
1.	Monitors water temperature and room temperature.

2.	Monitor feeding status via Blynk charts and Timers
	#Sends notifications when feeding due or over due (Lights green rectangle when feed still okay, orange when 1 day passed, red when >3 days past)
	
3. 	Monitor cleaning status
	#sends notifications when cleaning due, over due (Lights green smiley 😉, orange when 1 day passed 😐, red sad face when >3 days passed ☹)
	
4.	Motion Detection: Checks if lid is open/moved using the senseHat Gyroscope Pitch

5.	Security alarm: If lid moved, captures an image and sends it to Firebase DB. 
	Most Recent image can be viewed in the Glitch URL: https://angry-uttermost-gaura.glitch.me/

6.	SenseHat LED matrix as light source

RASPBERRY Pi SET UP:

<img src="https://user-images.githubusercontent.com/96552779/208763693-07f04aaf-10fb-4413-afcb-643c6e606d75.jpg" width=50% height=50%>

I am using a Raspberry Pi 4B 2gb which is attached on the Fish Tank's Lid.

I then attached a 2 way 40 pin extension header and connected both SenseHat and the Pins for the D18B20 Temperature sensors.

I used a breakout board and connected 2 D18B20 sensors on parallel connection. I opted not to use the breadboard and the resistors as they might be moved out of place whenever the fish tank lid is opened.

One DS18B20 temperature sensor goes inside the Fish tank to measure the Water Temperature and another DS18B20 temperature sensor placed outside the tank to measure the ambient temperature(Room temp). Initially I was planning on using the SenseHat temperature sensor to measure the room temperature but the sensor picks up the heat from the SenseHat and thus returning high temperature readings.

The DS18B20 temperature sensors are connected on one breakout board. This is possible using the One- Wire interface. One-Wire is a device communications bus system designed by Dallas Semiconductor Corp. that provides low-speed (16.3 kbit/s[1]) data, signaling, and power over a single conductor.

The DS18B20 sensor has 3 coloured wires. Red for power(VCC), Yellow for data, and Black for ground. The breakout board that came with the sensors has labels on it (VCC, data, ground). I used a female to female jumper wires to connect the breakout board to the RPi pins. The VCC is connected to the 3V3 (pin 1), the data wire to the GPIO4- I2C (pin 7) and ground wire to ground(pin 7). Please note that the One Wire interfaces needs and I2C pin.

I also used a PiCamera attachement and positioned it upright to capture an image whenever the lid is moved. The images from the PiCamera is then pushed to the FirebaseDB and then to the Glitch app.

<img src="https://user-images.githubusercontent.com/96552779/208764204-af776fb5-43e8-4e23-b499-2b8c831a3899.jpg" width=50% height=50%>

Whenever the Lid is moved, the Sensehat LED lights up Red and Blue and the PiCamera is activated to capture an Image. I used the SenseHat gyroscope's Pitch degrees readings to detect if the lid was moved. The Red/Blue lights and image capture will stop when the lid is closed(Flat position)

<img src="https://user-images.githubusercontent.com/96552779/208764066-b35ef9dc-fc74-44ac-a3c3-38adf36ce19d.gif" width=50% height=50%>



BLYNK:

Web Dashboard:

<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/blynkDash.png" width=50% height=50%>


On my web dashboard, I have 3 sets of buttons for the Light, Feed and Clean Switches. The LED widgets will light up corresponding to the switches toggled.

I also have Line Charts for the Water and Room Sensors and Bar charts to log in the Alarm Triggered function, Feed Log and the Cleaning Log. I have label widgets to show the date and time of the recent alarm trigger and labels showing the room and water status.

#Feed/CLeaning due widgets???

Aside from the web dashboard, I also have a Blynk mobile app with the Swtiches and Charts. If a Blynk Event is Triggered, I will receive a push notification on my mobile phone. A critical event will sound an Alarm.

DataStreams

<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/datastreams.png" width=50% height=50%>

Events


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/events.png" width=50% height=50%>


BLYNK MOBILE APP:
Mobile App DashBoard
<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/mobileapp2.png" width=33% height=33%>


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/mobileapp1.png" width=33% height=33%>


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/mobileapp3.png" width=33% height=33%>


FIREBASEDB:

Images captured during the alarm triggered event will be push and stored to the FirebaseDB


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/firebaseDB.png" width=50% height=50%>



REFERENCES/SOURCES:

https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0

https://pinout.xyz/

https://www.alamy.com/fish-tank-cartoon-image246642635.html

https://en.wikipedia.org/wiki/1-Wire
