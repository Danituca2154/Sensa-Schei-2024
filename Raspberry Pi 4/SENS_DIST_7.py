import RPi.GPIO as GPIO
import board
import time
import adafruit_vl6180x as vl6180
from libBNO055 import BNO055

 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# setup ToF ranging/ALS sensor

GPIO.setup(25,GPIO.OUT)                    # prendo il gpio del giroscopio è lo metto .out
GPIO.output(25,GPIO.LOW)

GPIO.setup(8,GPIO.OUT)                    # prendo il gpio del giroscopio è lo metto .out
GPIO.output(8,GPIO.LOW)

i2c = board.I2C()

class sensor:
	misura = None
	def define(self, pin = -1, address = -1):
		self.pin = pin
		self.address = address

class VL6180X:
	def __init__(self):
		self.k = 6
		self.laser = [sensor() for i in range(self.k)]
		self.laser[0].define(pin = 10, address = 0x20)
		self.laser[2].define(pin = 9, address = 0x21)
		self.laser[1].define(pin = 11, address = 0x22)   
		self.laser[3].define(pin = 25, address = 0x23)
		self.laser[4].define(pin = 8, address = 0x24)
		self.laser[5].define(pin = 7, address = 0x25)
		'''
		self.laser = [sensor() for i in range(6)]
		self.laser[0] = self.ds_fronte.define(pin = 10, address = 0x20)
		self.laser[1] = self.ds_sinistra_davanti.define(pin = 9, address = 0x21)
		self.laser[2] = self.ds_destra_davanti.define(pin = 11, address = 0x22)
		self.laser[3] = self.ds_destra_dietro.define(pin = 25, address = 0x23)
		self.laser[4] = self.ds_sinistra_dietro.define(pin = 8, address = 0x24)
		self.laser[5] = self.ds_retro.define(pin = 7, address = 0x25)
		'''
		
		
		for i in range(self.k):
			GPIO.setup(self.laser[i].pin,GPIO.OUT)
			GPIO.output(self.laser[i].pin,GPIO.LOW)
		
		for i in range(self.k):
			GPIO.output(self.laser[i].pin,GPIO.HIGH)
			time.sleep(0.1)
			ls = vl6180.VL6180X(i2c)
			ls._write_8(0x212, self.laser[i].address)
			time.sleep(0.1)
			self.laser[i].misura = vl6180.VL6180X(i2c, self.laser[i].address)
		print("Laser INIT finito")

	def read(self , n):
		misura = self.laser[n].misura.range
		return misura

if __name__ == '__main__':
	laser = VL6180X()
	bno = BNO055()
	

	if bno.begin() is not True:
		print("Error initializing device")
		exit()
		
	   
		
	while True:
		
		
		
		print(laser.read(0),laser.read(1),laser.read(2),laser.read(3),laser.read(4),laser.read(5),)
		
