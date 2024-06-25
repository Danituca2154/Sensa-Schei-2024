from time import sleep
import pigpio

import RPi.GPIO as GPIO

BUZZ = 12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
GPIO.setup(BUZZ, GPIO.OUT) #led scivolidestra

GPIO.output(22, GPIO.LOW)
GPIO.output(BUZZ, GPIO.LOW)


LED_D = 22
LED_S = 22
#BUZZ = 12
standard = 1530
sinistra = 2200
destra = 880

'''
old valori 1650, 2200, 1150
'''


class Servo:
	
	def init(self):
		self.SERVO = 18
		self.pi = pigpio.pi()
		self.pi.set_mode(self.SERVO, pigpio.OUTPUT)
		self.pi.set_servo_pulsewidth(self.SERVO, standard) # posizione neutra
		self.contatore = 0
		
	def sinistra(self):
		if self.contatore < 12:
			self.pi.set_servo_pulsewidth(self.SERVO, sinistra) # posizione massima
			sleep(0.5)
			self.pi.set_servo_pulsewidth(self.SERVO, standard) # posizione neutra
			sleep(0.5)
			self.contatore += 1 
			print(self.contatore)
	def destra(self):
		if self.contatore < 12:
			self.pi.set_servo_pulsewidth(self.SERVO, destra) # posizione minima
			sleep(0.5)
			self.pi.set_servo_pulsewidth(self.SERVO, standard) # posizione neutra
			sleep(0.5)
			self.contatore += 1 
			print(self.contatore)
		
				
	def H_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("H_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def H_destra(self):	
		GPIO.output(LED_D, GPIO.HIGH)	
		print("H_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	

	def S_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("S_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def S_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)	
		print("S_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		
	def U_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("U_S")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
				
	def U_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("U_D")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)

	def rosso_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("Rosso_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def rosso_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)	
		print("Rosso_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()
		
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)

	def giallo_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)	
		print("Giallo_S")
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.sinistra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)

	def giallo_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)	
		print("giallo_D")
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)	
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		self.destra()	
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)	
		sleep(0.5)	
		
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)

	def verde_sinistra(self):
		GPIO.output(LED_S, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("Verde_S")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_S, GPIO.LOW)
		
	def verde_destra(self):
		GPIO.output(LED_D, GPIO.HIGH)
		GPIO.output(BUZZ, GPIO.HIGH)
		print("Verde_D")
		sleep(0.5)
		GPIO.output(BUZZ, GPIO.LOW)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(LED_D, GPIO.LOW)
		

if __name__ == '__main__':
	servo = Servo()
	servo.init()
	
	while True:
		'''
		#servo.destra()
		print(servo.contatore)
		#sleep(1)
		servo.sinistra()
		sleep(1)
		'''
		servo.H_destra()
		sleep(1)
		servo.H_sinistra()
		sleep(1)
		servo.rosso_sinistra()
		sleep(1)
		servo.giallo_destra()
		sleep(1)
		
		
