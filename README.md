# projectfishtank
Project fishtank
Student Name: Eugenio Manlapaz
Student ID: 20100013
Project Repo: https://github.com/emanlapaz/projectfishtank

Introduction:
	Project fishtank is an IOT project using the Raspberry pi. Tropical aquarium fish needs a certain temperature range to be healthy and reproduce. Proper cycling of light and water is also very essential same as with the feeding schedule. The aim of this project is to use the Raspberry Pi to monitor activities such as feeding and cleaning, temperature (ambient and water temperature), and any unwanted events that could happen ( e.g. a toddler opening the lid and pouring all the feed inside the tank).
 
Materials:
1.	Raspberry pi
2.	Sense Hat
a.	LED matrix for displays
b.	Temperature sensor for ambient room temperature
c.	Gyroscope for lid opening
d.	Joystick
3.	Camera
4.	Waterproof temperature probe (submerged in tank)
5.	Optional: Energenie Pi mote (optional to control the fish tank light cycles) or TPlink Kasa smart plugs

Tech:
1.	Wi-Fi
2.	Thingspeak for stats
a.	Water temperature
b.	Ambient temperature
c.	Feed pattern (dates done)
d.	Cleaning pattern (dates done)
3.	Blynk for Mobile app connection

Applications:
1.	Monitors water temperature(using waterproof temp sensor) and ambient temperature using the sensehat temperature sensor.
2.	Monitor feeding status. Sends notifications when feeding due or over due (Lights green rectangle when feed still okay, orange when 1 day passed, red when >3 days past)
3.	 Monitor cleaning status sends notifications when cleaning due, over due (Lights green smiley 😉, orange when 1 day passed 😐, red sad face when >3 days passed ☹)
4.	Check if lid is open(uses)
a.	If lid open and joystick pressed up, feeding
b.	If lid open and joystick pressed down, tank cleaning
c.	Security alarm: If lid open and joystick not pressed, light up after 1 minute, send notification and capture photo via camera
5.	Check feed and cleaning status using the joystick and displays on the LED matrix
a.	Right feed status- days due/ days overdue
b.	Left cleaning status- days due/ days overdue
6.	Optional: Controls the light source for day and night cycling.


REFERENCES: