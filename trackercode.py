#python 3.7.3
#import _thread 
import time
from datetime import datetime

import serial 
import requests 
from micropyGPS import MicropyGPS 
import firebase_admin #GOOGL
import Adafruit_SSD1306 

import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

print("program started")

#screen related
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
disp =Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

font = ImageFont.load_default()
image = Image.new("1",(disp.width,disp.height))
draw = ImageDraw.Draw(image)
draw.text((0, 0), "hello! waiting 60",  font=font, fill=255)
draw.text((0,8),"sec for the gps to",font=font,fill=255)
draw.text((0,16),"connect to sat",font=font,fill=255)
disp.image(image)
disp.display()
#end screen related


#gps related
s=serial.Serial('/dev/ttyS0',9600)

dump = s.readline() #always reads gibberish when it starts

my_gps = MicropyGPS()
my_sentence = '$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62' #should look like this

latitude = ''
longitude = ''
altitude = ''
speed = ''
satellites = ''
#end gps-related

#data logging related
#end data logging related

time.sleep(60) #making it wait 60 seconds before reading data to make sure
#that the GPS is connected to satellites - making it idiotproof 

while True:
	try:
		#gps related
		c=s.readline().decode('utf-8')
		#print(c)
		time.sleep(0.6) #GPS refresh rate is about 1hz - avoiding unnecessary computations
		for x in c:
			
			my_gps.update(x)
			
			latitude = my_gps.latitude_string()
			longitude = my_gps.longitude_string()
			altitude = str(my_gps.altitude)
			speed = my_gps.speed_string('kph')
			satellites = str(my_gps.satellites_in_use)
			speed2 = speed.replace(" km/h","")
		
			#print(" lat:"+latitude+" lon:"+longitude+" alt:"+altitude+" spd:"+speed2+" sat:"+satellites)
		#end gps related
		
		#screen related
		spdalt = "spd:" + str(int(float(speed2))) + " alt:" + altitude 
		satstr = "satellites: " + satellites

		disp.clear()
		image1 = Image.new("1",(disp.width,disp.height))
		draw = ImageDraw.Draw(image1)
		#draw.text((0, 0), "test",  font=font, fill=255)
		draw.text((0, 0), longitude, font = font, fill=255)
		draw.text((0, 8), latitude, font = font, fill=255)
		draw.text((0, 16), spdalt, font = font, fill=255)
		draw.text((0,24), satstr, font = font, fill=255)
		disp.image(image1)
		disp.display()
		#end screen related
	
		#logging related
		datetimeobj=datetime.now()
		datetimev = datetimeobj.strftime("%d/%m/%Y (%H:%M:%S)")
		logstring = latitude + '|' + longitude + '|' + str(int(float(speed2))) + '|' + altitude + '|' + datetimev + '\n' 
		#print(logstring)
		logfile = open('GPSlog.txt','a')
		logfile.write(logstring)
		logfile.close()
		#end logging related


	except:
		print("Error!")

