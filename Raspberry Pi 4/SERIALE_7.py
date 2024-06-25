import serial
import time
from time import sleep
import struct

class Serial:
	
	def __init__(self):
		self.ser = serial.Serial(
			port='/dev/ttyAMA0',
			baudrate = 500000,
			parity = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			timeout = 0
		)
		self.error = "serial error"
		self.fermo = 10
		self.avanti = 1
		self.destra = 2
		self.sinistra = 3
		self.indietro = 4
		self.destra_veloce = 5
		self.sinistra_veloce = 6
		
		
		self.svuotaimpulsi = 20
		
		self.piastrecol = 40
		
		self.destraa90 = 60
		self.sinistraa90 = 70
		
		self.setpoint = 100
		self.setpointPIU = 110
		self.setpointMENO = 120
		self.setsini = 130
		self.setdest = 140
		
		self.cm30 = 150
		self.salitee = 160
		self.discesee = 170
		self.salitainversaa = 180
		self.discesainversaa = 190
		
		self.variabile = 200
	'''
	def read(self, byte = 2):
	 bn  
		readbyte = self.ser.read(size = byte)
		print(readbyte)
		
	
		'''
		
	def read(self, byte = 1):
		#self.clean()
		start = time.time()
		out = 0
		while(self.ser.in_waiting <= 0):
			if((time.time() - start) > 0.05):
				#print(self.error)
				out = self.error
				break
		if out != 69:
			readbyte = self.ser.read(size = byte)
			if (len(readbyte) != byte):
				#print(self.error)
				out = self.error
			else:
				out = 0
				for i in range(byte):
					out |= readbyte[i]<<(8*i) #+ (readbyte[1]<<8)
		return(out)

	def write(self, byte): 
		self.ser.write(struct.pack('>B',byte))
	#--------------------------------------------------------------------------------------------------------		
	def setsetpoint(self):
		byteOut = self.setpoint	
		self.write(byteOut)
	def setsetpointPIU90(self):
		byteOut = self.setpointPIU	
		self.write(byteOut)
	def setsetpointMENO90(self):
		byteOut = self.setpointMENO	
		self.write(byteOut)
	def setdes(self):
		byteOut = self.setdest
		self.write(byteOut)
	def setsin(self):
		byteOut = self.setsini
		self.write(byteOut)
	#--------------------------------------------------------------------------------------------------------		
	def cm(self):
		impulsi=0
		byteOut = self.cm30	
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	#--------------------------------------------------------------------------------------------------------		
	def salite(self):
		impulsi=0
		byteOut = self.salitee	
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	def salitainversa(self):
		impulsi=0
		byteOut = self.salitainversaa		
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	#--------------------------------------------------------------------------------------------------------		
	def discese(self):
		impulsi=0
		byteOut = self.discesee	
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	def discesainversa(self):
		impulsi=0
		byteOut = self.discesainversaa	
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	#---------------------------------------------------------------------------------
	def setavanti(self):
		impulsi=0
		byteOut = self.avanti
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	#------------------------------------------------------------------------------------------------------------
	def setindietro(self):
		impulsi=0
		byteOut = self.indietro
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	#---------------------------------------------------------------------------------------------------------------
	def setdestra(self):
		byteOut = self.destra
		self.write(byteOut)
	#---------------------------------------------------------------------------------------------------------------
	def setdestraveloce(self):
		byteOut = self.destra_veloce
		self.write(byteOut)
	#---------------------------------------------------------------------------------------------------------------
	def setsinistra(self):
		byteOut = self.sinistra
		self.write(byteOut)
	#---------------------------------------------------------------------------------------------------------------
	def setsinistraveloce(self):
		byteOut = self.sinistra_veloce
		self.write(byteOut)
	#---------------------------------------------------------------------------------------------------------------
	def setfermo(self):
		byteOut = self.fermo
		self.write(byteOut)
		
	def setfermoflag(self):
		byteOut = self.fermo
		self.write(byteOut)
	#-------------------------------------------------------------------------------------------------------------
	def azzeroimpulsi(self):
		byteOut = self.svuotaimpulsi
		self.write(byteOut)
		self.clean()
		controllo = self.read()
		return controllo
	#--------------------------------------------------------------------------------------------------------------
	def piastre(self):
		byteOut = self.piastrecol
		self.write(byteOut)
		self.clean()
		colore = self.read()
		return colore
	#--------------------------------------------------------------------------------------------------------------
	def destra90(self):
		byteOut = self.destraa90	
		self.write(byteOut)
		self.clean()
		fatto = self.read()
		return fatto
	#--------------------------------------------------------------------------------------------------------------
	def sinistra90(self):
		byteOut = self.sinistraa90	
		self.write(byteOut)
   
	def finegiro(self):
		byteOut = self.variabile
		self.write(byteOut)
		fatto = self.read()
		return fatto
   
   
	def clean(self):
		self.ser.flush()
		self.ser.flushInput()


if __name__ == '__main__':  
	serial = Serial()
	sleep(1)
	


	while True:	
		
		
		serial.setavanti(3000, 3000)
		#print(serial.read())
		
		#serial.write(57)	print(serial.read())
		#sleep(4)
		
		#serial.write(11)	
		#serial.read()
		sleep(0.1)
		
		#print("------------")
