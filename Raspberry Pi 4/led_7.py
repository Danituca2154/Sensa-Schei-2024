import RPi.GPIO as GPIO
from time import sleep


class Led:
	import RPi.GPIO as GPIO
	def __init__(self):
		self.GPIO.setmode(GPIO.BCM)
		self.GPIO.setwarnings(False)
		self.GPIO.setup(4, GPIO.OUT)
		self.GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
		self.GPIO.setup(12, GPIO.OUT) #led scivolidestra
		self.GPIO.setup(5, GPIO.OUT)
		self.GPIO.setup(6, GPIO.OUT)# buzz


		self.GPIO.output(4, GPIO.LOW)
		self.GPIO.output(22, GPIO.LOW)
		self.GPIO.output(6, GPIO.LOW)


		self.LED_Colori= 4
		self.LED_Cam = 22
		self.LED_S = 12
		self.LED_D = 5
		self.BUZZ = 6

	

	
	def tutti_led_ON(self):
	
		#self.GPIO.output(self.LED_Colori, self.GPIO.HIGH)
		self.GPIO.output(self.LED_Cam, self.GPIO.HIGH)
		self.GPIO.output(self.LED_S, self.GPIO.HIGH)
		self.GPIO.output(self.LED_D, self.GPIO.HIGH)
		#self.GPIO.output(self.BUZZ, self.GPIO.HIGH)

		
		
		
	def tutti_led_OFF(self):
	
		self.GPIO.output(self.LED_Colori, self.GPIO.LOW)
		self.GPIO.output(self.LED_Cam, self.GPIO.LOW)
		self.GPIO.output(self.LED_S, self.GPIO.LOW)
		self.GPIO.output(self.LED_D, self.GPIO.LOW)
		self.GPIO.output(self.BUZZ, self.GPIO.LOW)
		
	def led_cam_ON(self):
		self.GPIO.output(self.LED_Cam, self.GPIO.HIGH)
		
	def led_cam_OFF(self):
		self.GPIO.output(self.LED_Cam, self.GPIO.LOW)
		
	def led_sotto_ON(self):
		self.GPIO.output(self.LED_Colori, self.GPIO.HIGH)
		
	def led_sotto_OFF(self):
		self.GPIO.output(self.LED_Colori, self.GPIO.LOW)
		
		
		
if __name__ == '__main__':
	led = Led()
	led.tutti_led_OFF()
	sleep(5)
	while True:
		try:
			led.led_sotto_ON()
			led.led_cam_ON()
		except KeyboardInterrupt:
			tutti_led_OFF()
