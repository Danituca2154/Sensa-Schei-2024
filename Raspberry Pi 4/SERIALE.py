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
		
		self.svutaimpulsi = 20
		
		self.piastrecol = 40
		
		self.destraa90 = 60
		self.sinistraa90 = 70
		
		self.setpoint = 100
		self.setpointPIU = 110
		self.setpointMENO = 120
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
	def setsetpoint():
		byteOut = self.setpoint	
		self.write(byteOut)
	def setsetpointPIU90():
		byteOut = self.setpointPIU	
		self.write(byteOut)
	def setsetpointPIUMENO():
		byteOut = self.setpointPIU	
		self.write(byteOut)
	#---------------------------------------------------------------------------------
	def setavanti(self):
		impulsi=0
		byteOut = self.avanti
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		#print('ecco',impulsi)
		if impulsi == 69:
			self.clean()
		return impulsi
	#------------------------------------------------------------------------------------------------------------
	def setindietro(self, velocita):
		impulsi=0
		byteOut = self.indietro
		self.write(byteOut)
		self.clean()
		impulsi = self.read()
		return impulsi
	#---------------------------------------------------------------------------------------------------------------
	def setdestra(self, velocita):
		byteOut = self.destra
		self.write(byteOut)
	#---------------------------------------------------------------------------------------------------------------
	def setsinistra(self, velocita):
		byteOut = self.sinistra
		self.write(byteOut)
	#---------------------------------------------------------------------------------------------------------------
	def setfermo(self, velocita):
		byteOut = self.fermo()
		self.write(byteOut)
		
	def setfermoflag(self, velocita):
		byteOut = self.fermo()
		self.write(byteOut)
	#-------------------------------------------------------------------------------------------------------------
	def azzeroimpulsi(self):
		byteOut = self.svuotaimpulsi
		self.write(byteOut)
	#--------------------------------------------------------------------------------------------------------------
	def piastre(self):
		byteOut = self.piastrecol
		self.write(byteOut)
		self.clean()
		colore = self.read()
		return colore
	#--------------------------------------------------------------------------------------------------------------
	def destra90():
		byteOut = self.destraa90	
		self.write(byteOut)
	#--------------------------------------------------------------------------------------------------------------
	def sinistra90():
		byteOut = self.sinistraa90	
		self.write(byteOut)
   
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
