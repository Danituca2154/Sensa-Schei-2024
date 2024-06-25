import RPi.GPIO as GPIO
import subprocess
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

pulsante = 23

commando1 = 'cd /home/sensaschei2/Desktop/MACCHININA 7'

commando2 = 'python3 LAMAPPADEFINITIVA.py'



controllo = 0

def button_callback(channel):
	global controllo
	print (controllo)
	if (controllo == 0):
		print( "START")
		subprocess.call(commando1, shell=True)
		sleep(0.1)
		subprocess.call(commando2, shell=True)
		controllo = 1
		
	
GPIO.add_event_detect(pulsante, GPIO.FALLING, callback=button_callback, bouncetime = 100)

while True:
	pass
