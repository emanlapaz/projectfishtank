Project FishTank IOT

<img src="https://user-images.githubusercontent.com/96552779/208731692-a823ca14-21fd-4e9c-94e2-146962f121f7.jpg" width=50% height=50%>




Student Name: Eugenio Manlapaz

Student ID: 20100013

Project Repo: https://github.com/emanlapaz/projectfishtank

Glitch URL: https://angry-uttermost-gaura.glitch.me/

Youtube Video Link: https://youtu.be/JSSJBrVIrxI

PROJECT INFOGRAPHIC:


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/Fishtank%20slide%20pic.jpg" width=100% height=100%>



INTRODUCTION:

Project fishtank is an IOT project using the Raspberry pi. Tropical aquarium fish needs a certain temperature range to be healthy and reproduce. Proper cycling of light and water is also very essential same as with the feeding schedule. The aim of this project is to use the Raspberry Pi to monitor activities such as feeding and cleaning, temperature (ambient and water temperature), and any unwanted events that could happen ( e.g. a toddler opening the lid and pouring all the feed inside the tank).
 
 
 <img src="https://user-images.githubusercontent.com/96552779/208762335-36238a13-1587-444e-b57f-d73847afb687.gif" width=50% height=50% >
 
 
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

3. Feed Monitor/ Logger. When the feed switch from the Blynk dash is turned on, logs the date and time on the charts. This will turn off the Alarm funtion and gives a prompt whenever the alarm is deactivated. The sensehat LED will show a message and displays a smiley. A countdown will start on the background. When the timer is done, will turn off the feed switch and activate the alarm function, displays a message and a sad face on the sensehat LED.

	Video link: https://youtu.be/AAjUQZmRiLY

4. Cleaning Monitor/ Logger. When the clean switch from the Blynk dash is turned on, logs the date and time on the charts. This will turn off the Alarm funtion and gives a prompt whenever the alarm is deactivated. The sensehat LED will show a message and displays a smiley. A countdown will start on the background. When the timer is done, will turn off the clean switch and activate the alarm function, displays a message and a sad face on the sensehat LED.

	Video link: https://youtu.be/q87TbEKqARE

5. Alarm/Movement Detection using SenseHat Gyroscope. When the Fish Tank lid is tilted (pitch up) activates the alarm, flashes led lights and starts capturing images until the lid is placed on a flat position. 

	Video link: https://youtube.com/shorts/WokquJIVTvg

Applications:
1.	Monitors water temperature and room temperature.

2.	Monitor feeding status via Blynk charts
	
3. 	Monitor cleaning status using charts
	
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

The DS18B20 temperature sensors are connected on one breakout board. This is possible using the One- Wire interface. One-Wire is a device communications bus system designed by Dallas Semiconductor Corp. that provides low-speed (16.3 kbit/s[1]) data, signaling, and power over a single conductor. (Wikipedia)

The DS18B20 sensor has 3 coloured wires. Red for power(VCC), Yellow for data, and Black for ground. The breakout board that came with the sensors has labels on it (VCC, data, ground). I used a female to female jumper wires to connect the breakout board to the RPi pins. The VCC is connected to the 3V3 (pin 1), the data wire to the GPIO4- I2C (pin 7) and ground wire to ground(pin 7). Please note that the One Wire interfaces needs and I2C pin.

I also used a PiCamera attachement and positioned it upright to capture an image whenever the lid is moved. The images from the PiCamera is then pushed to the FirebaseDB and then to the Glitch app.

<img src="https://user-images.githubusercontent.com/96552779/208764204-af776fb5-43e8-4e23-b499-2b8c831a3899.jpg" width=50% height=50%>

Whenever the Lid is moved, the Sensehat LED lights up Red and Blue and the PiCamera is activated to capture an Image. I used the SenseHat gyroscope's Pitch degrees readings to detect if the lid was moved. The Red/Blue lights and image capture will stop when the lid is closed(Flat position)

<img src="https://user-images.githubusercontent.com/96552779/208764066-b35ef9dc-fc74-44ac-a3c3-38adf36ce19d.gif" width=50% height=50%>



BLYNK:

Web Dashboard:

<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/new_dash.png" width=50% height=50%>


On my web dashboard, I have 3 sets of buttons for the Light, Feed and Clean Switches. The LED widgets will light up corresponding to the switches toggled. The Feed and Clean Switch will hold the Alarm system and will not light up and capture an image when the fishtank lid is removed

I also have Line Charts for the Water and Room Sensors and Bar charts to log in the Alarm Triggered function, Feed Log and the Cleaning Log. I have label widgets to show the date and time of the recent alarm trigger and labels showing the room and water status.


Aside from the web dashboard, I also have a Blynk mobile app with the Swtiches and Charts. If a Blynk Event is Triggered, I will receive a push notification on my mobile phone. A critical event will sound an Alarm.

DataStreams:

I used multiple datastreams to build my Blynk app. I used Integer, String and Enumerable for the data types.


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/datastreams.png" width=50% height=50%>


Events

The Events serves as the main notification function for this IOT project. I have set Alarm triggered function to Critical Event. This will push a notification to my mobile device (push notification plus alarm sound) when the alarm is tripped. There are also set events for the temperature sensors.

<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/events.png" width=50% height=50%>


BLYNK MOBILE APP:
Mobile App DashBoard


Mobile app switches


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/mobileapp1.png" width=33% height=33%>



Mobile app charts


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/mobileapp2.png" width=33% height=33%>



Mobile app Notifications


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/mobileapp3.png" width=33% height=33%>


FIREBASEDB:

Images captured during the alarm triggered event will be push and stored to the FirebaseDB


<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/firebaseDB.png" width=50% height=50%>



GLITCH:

The Glitch website displays the most recent images taken.

<img src="https://github.com/emanlapaz/projectfishtank/blob/main/images/monkey.png" width=50% height=50%>


ISSUES/BUGS:
The SenseHat plus the temperature sensor slows down the return values. I might have been overloading the RPi processor with my current set up. The SenseHat gyroscope returns multiple values per second, any changes in orientation will be reflected in realtime if the sensehat is running on its own.

Adding the temperature readings from the DS18B20 sensors slows down the gyroscope readings drastically and the gyroscope readings will try to catch up. Adding additional functions will further slow down the gyroscope readings.

I was planning to toggle on/off the gyroscope readings(which triggers my ALARM event) but unfortunately I was not quite successful. Instead, I added a Countdown timer function to override(hold) the gyroscope readings thus preventing the ALARM function to be triggered. This work around is functional but not very efficient.

TO DOS/ IMPROVEMENTS:
1. Use a motion sensor instead of the sensehat gyroscope
2. Try threading if it works
3. Add feed/cleaning due timers- notifies when feed/cleaning due
4. Display multiple captured images on the Glitch APP

INSTRUCTIONAL VIDEOS:

SenseHat: https://youtu.be/lRQ48V8p06k

Ds18B20 temperature sensors: https://youtu.be/j7LLVkPpQ78


REFERENCES/SOURCES:

https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0

https://pinout.xyz/

https://www.alamy.com/fish-tank-cartoon-image246642635.html

https://en.wikipedia.org/wiki/1-Wire
