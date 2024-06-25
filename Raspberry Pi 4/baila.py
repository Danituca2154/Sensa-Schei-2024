from time import sleep
from libBNO055 import BNO055
from SERIALE_7 import Serial
from SENS_DIST_7 import VL6180X
from led_7 import Led
import RPi.GPIO as GPIO
from piastre2_7 import APDS9960
import asyncio
from multiprocessing import Process, Queue
queue = Queue()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)# led scivoli sinistra
GPIO.setup(12, GPIO.OUT) #led scivolidestra
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)# buzz
GPIO.setup(17, GPIO.OUT)

destra = 13
centro = 16
sinistra = 19
dietro = 20
GPIO.setup(destra, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)# fc1 destra
GPIO.setup(centro, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)# fc2 centro
GPIO.setup(sinistra, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)# fc3 sinistra
GPIO.setup(dietro, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)# fc4 dietro


class Movimenti:
	def init(self):
		self.pin_digitale_1 = 27
		GPIO.setup(self.pin_digitale_1, GPIO.OUT)
		GPIO.output(self.pin_digitale_1, GPIO.LOW)
		
		self.pin_digitale_2 = 17
		GPIO.setup(self.pin_digitale_2, GPIO.OUT)
		GPIO.output(self.pin_digitale_2, GPIO.LOW)
		
		self.ser= Serial()
		self.piastre = APDS9960()
		self.bno = BNO055()
		self.led = Led()
		self.laser = VL6180X()
		self.bno.begin()
	
	def dritta(self):
			if(self.laser.read(1) < 50 and (self.laser.read(4)+9)<50):
				self.ser.setdestraveloce()
				print('ok')
				sleep(0.4)
			if(self.laser.read(2) < 50 and (self.laser.read(3))<50):
				self.ser.setsinistraveloce()
				print('si33')
				sleep(0.4)	
			if(self.laser.read(1) <120 and (self.laser.read(4)+10)>70 and (self.laser.read(4)+10)<170): # sx dav, sx dietro, sx dietro
					while((self.laser.read(1)/(self.laser.read(4)+10))<0.94):
						self.ser.setdestra()
			self.ser.setfermo()
			sleep(0.01)
			
			if((self.laser.read(4)+10) <120 and self.laser.read(1)>70 and self.laser.read(1)<170): # sx dietro, sx dav, sx dav
				while((self.laser.read(4)+10)/(self.laser.read(1))<0.94):
					self.ser.setsinistra()
			self.ser.setfermo()
			sleep(0.01)
			if(self.laser.read(2) <120 and (self.laser.read(3)+13)>70 and (self.laser.read(3)+13)<170): # dx dav, dx dietro, dx dietro
				while((self.laser.read(2)/(self.laser.read(3)+13))<0.94):
					self.ser.setsinistra()
			self.ser.setfermo()
			sleep(0.01)
			if((self.laser.read(3)+13) <120 and self.laser.read(2)>70 and self.laser.read(2)<170):
				while(((self.laser.read(3)+13)/self.laser.read(2))<0.94):
					self.ser.setdestra()
			self.ser.setfermo()
			sleep(0.01)
	
	def riposizionamento(self):
		while (GPIO.input(dietro) == False):
			flag = get_flag()
			if not flag:
				self.ser.setindietro()
				self.ser.clean()
			else:
				self.ser.setfermoflag()
				self.ser.clean()
		self.ser.clean()
		self.ser.setsetpoint()
		sleep(0.05)
		self.impulsi=0
		controllo = self.ser.azzeroimpulsi()
		while controllo == 'serial error':
			controllo = self.ser.azzeroimpulsi()
		#print('fatta bro')
		self.ser.clean()
		while (self.impulsi < 30):
			self.impulsi = self.ser.setavanti()
			if self.impulsi=='serial error':
				self.impulsi = 0
			sleep(0.01)
		self.ser.clean()
		self.ser.setfermo()
		self.ser.setfermo()
		sleep(0.1)		
	
	def destra(self):
		self.ser.setsetpointPIU90()
		sleep(0.01)
		self.ser.destra90()
		des = 0
		while (des!=70):
			flag = get_flag()
			if not flag:
				des = self.ser.finegiro()
				#print(des)
				GPIO.output(17, GPIO.LOW)
				#if (des==80):
					#break
			else:
				GPIO.output(17, GPIO.HIGH)
				#print('FERMAAAA')
		print(des)

	def sinistra(self):
		self.ser.setsetpointMENO90()
		sleep(0.01)
		#print('meno90')
		self.ser.sinistra90()
		#print('sinistra90')
		sin = 0
		while (sin!=70):
			#print('dentro while')
			sin = self.ser.finegiro()
			flag = get_flag()
			if not flag:
				sin = self.ser.read()
				#print(sin)
				GPIO.output(17, GPIO.LOW)
				#if (sin==70):
					#break
			else:
				GPIO.output(17, GPIO.HIGH)
				#print('FERMAAAA')
		print(sin)
		
	async def first_task(self):
		nuova_cella = True
		self.ferma_cicli = False
		self.salita = False
		while (self.ferma_cicli == False):
			self.ser.clean()
			self.ser.cm()
			imp=0
			while ((imp<230) and (self.ferma_cicli == False)):
				flag = get_flag()
				if not flag:
					imp = self.ser.cm()
					if imp == 'serial error':
						imp = 20
					if imp > 100 and nuova_cella:    # condizione per capire in quale cella sta la vittima
						with open('valore.txt', 'r') as file:
							index_next_cell = int(file.readline().strip())
						queue.put('cella')
						queue.put(index_next_cell)
						nuova_cella = False
						self.cella_successiva = True
					await asyncio.sleep(0.001)
				else:
					self.ser.setfermoflag()
					self.ser.clean()
					await asyncio.sleep(0.001)
			
			if imp >= 230:
				if(self.laser.read(0) > 45 and self.laser.read(0) < 124):
					while (self.laser.read(0) > 65 and self.laser.read(0) < 124):
						self.ser.cm()
						print("ecoooooooooooooooooooooooooo")
					self.ser.setfermo()
					controllo = self.ser.azzeroimpulsi()
					while controllo == 'serial error':
						controllo = self.ser.azzeroimpulsi()
				self.ser.clean()
				self.ser.setfermo()
				self.ferma_cicli = True
				break
			await asyncio.sleep(0.001)
		return '30cm'
	async def second_task(self):
		self.ferma_cicli = False
		while (self.ferma_cicli == False):
			self.nero = self.piastre.prova()
			self.inclinazione = self.bno.inclinazione()
			if self.nero=='nero':
				print("piastra nera")
				self.situazione = 'nero'
				self.ferma_cicli = True
			if (GPIO.input(centro) == True or GPIO.input(destra) == True or GPIO.input(sinistra) == True):  #centro destra sinistra
					if  (GPIO.input(destra) == True and GPIO.input(sinistra) == False):  
						self.situazione = 'finecorsa destra'
					elif  (GPIO.input(sinistra) == True and GPIO.input(destra) == False):
						self.situazione = 'finecorsa sinistra'
					else:
						self.situazione = 'finecorsa'
					self.ferma_cicli = True
			
			if (self.inclinazione < -15):
				self.situazione = 'salita'
				self.ferma_cicli = True
			if (self.inclinazione > 20):
				self.situazione = 'discesa'
				self.ferma_cicli = True
			await asyncio.sleep(0.001)
		
		
	async def main(self):
		results = await asyncio.gather(self.first_task(), self.second_task())
		self.first_task_result, self.second_task_result = results
	def cm30(self):
		self.dritta()
		self.incliiniz = self.bno.inclinazione()
		self.ser.setsetpoint()
		self.situazione = 0
		self.cella_successiva = False
		self.ferma_cicli = False
		self.led.led_sotto_ON()
		self.led.led_cam_ON()
		self.impulsi = 0	
		self.ser.azzeroimpulsi()
		sleep(0.001)
		while True:
			asyncio.run(self.main())
			if (self.second_task_result == 'nero') or (self.second_task_result == 'finecorsa') or (self.first_task_result == '30cm'):
				break
		self.ser.setfermo()
		########################################## DISCESA #######################################################
		if self.situazione == 'discesa':
			self.inclinazione = self.bno.inclinazione()
			p = True
			l = True
			while (self.inclinazione>9) or (self.inclinazione<-30) or (self.inclinazione ==-0.0625):
				lettura_sinistra = self.laser.read(1)
				lettura_destra = self.laser.read(2)
				if self.nero=='nero':
					print("piastra nera in discesa")
					break
				if (lettura_sinistra<90 and p == True):
					self.ser.setsin()
					p = False
					l = True
				if (lettura_destra<90 and l == True):
					self.ser.setdes()
					p = True
					l = False
				self.ser.discese()
				self.inclinazione = self.bno.inclinazione()
				self.nero = self.piastre.provasalita()
			#--------------- TROVO IL NERO MENTRE FACCIO DISCESA -------------------
			if self.nero=='nero':
				if ((p == True) and (l == False)):
					self.ser.setsin()
				if ((p == False) and (l == True)):
					 self.ser.setdes()
				p = True
				l = True
				self.ser.setindietro()
				sleep(1)
				self.inclinazione = self.bno.inclinazione()
				while (self.inclinazione>9) or (self.inclinazione<-30) or (self.inclinazione ==-0.0625):
					lettura_sinistra = self.laser.read(3)
					lettura_destra = self.laser.read(4)
					if (lettura_destra<100 and p == True):
						self.ser.setdes()
						p = False
						l = True
					if (lettura_sinistra<80 and l == True):
						self.ser.setsin()
						p = True
						l = False
					self.inclinazione = self.bno.inclinazione()
					self.ser.salitainversa()
					sleep(0.01)
				self.ser.setindietro()
				sleep(1)
				self.situazione='nerosalita'
			else:
				self.ser.setavanti()
				sleep(0.5)
			self.nero = 0
			self.ser.setfermo()
			print("discesa")
		########################################## SALITA #######################################################
		if self.situazione == 'salita':
			self.inclinazione = self.bno.inclinazione()
			p = True
			l = True
			while (self.inclinazione<-4) or (self.inclinazione ==-0.0625):
				lettura_sinistra = self.laser.read(1)
				lettura_destra = self.laser.read(2)
				if self.nero=='nero':
					print("piastra nera in salita")
					break
				if (lettura_sinistra<70 and p == True):
					self.ser.setsin()
					p = False
					l = True
				if (lettura_destra<70 and l == True):
					self.ser.setdes()
					p = True
					l = False
				self.ser.salite()
				self.inclinazione = self.bno.inclinazione()
				self.nero = self.piastre.provasalita()
			#--------------- TROVO IL NERO MENTRE FACCIO SALITA -------------------
			if self.nero=='nero':
				if ((p == True) and (l == False)):
					self.ser.setsin()
				if ((p == False) and (l == True)):
					 self.ser.setdes()
				p = True
				l = True
				self.ser.setindietro()
				sleep(1)
				self.inclinazione = self.bno.inclinazione()
				while (self.inclinazione<-4) or (self.inclinazione ==-0.0625):
					lettura_sinistra = self.laser.read(3)
					lettura_destra = self.laser.read(4)
					if (lettura_destra<100 and p == True):
						self.ser.setdes()
						p = False
						l = True
					if (lettura_sinistra<80 and l == True):
						self.ser.setsin()
						p = True
						l = False
					self.inclinazione = self.bno.inclinazione()
					self.ser.discesainversa()
					sleep(0.01)
				self.ser.setindietro()
				sleep(0.5)
				self.situazione='nerosalita'
			else:
				self.ser.setavanti()
				sleep(0.5)
			self.nero = 0
			self.ser.setfermo()
			print("salita")
		########################################## FINECORSA DESTRA #######################################################
		if self.situazione == 'finecorsa destra':
			if self.laser.read(0)>15:
				#print('finecorsa destra')
				self.ser.azzeroimpulsi()
				sleep(0.01)
				self.impulsi2=0
				while (self.impulsi2 < 60):
					self.impulsi2 = self.ser.setindietro()
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.ser.setfermo()
				self.bno.begin()
				gradi = self.bno.readAngle()
				while (gradi > 351) or (0 <= gradi <= 2) or (gradi < 1) or (gradi > 361):
					self.ser.setsinistraveloce()
					gradi = self.bno.readAngle()
				self.ser.setfermo()
				if not self.cella_successiva:
					self.situazione = 'fine finecorsa'
				else:
					self.situazione = 0
			else:
				self.situazione = 'finecorsa'
			self.ser.setfermo()
		########################################## FINECORSA SINISTRA #######################################################
		if self.situazione == 'finecorsa sinistra':
			if self.laser.read(0)>15:
				#print('finecorsa sinistra')
				self.ser.azzeroimpulsi()
				sleep(0.01)
				self.impulsi2=0
				while (self.impulsi2 < 60):
					self.impulsi2 = self.ser.setindietro()
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.ser.setfermo()
				self.bno.begin()
				gradi = self.bno.readAngle()
				while (gradi < 9) or (358 <= gradi <= 360) or (gradi < 1) or (gradi > 361):
					self.ser.setdestraveloce()
					gradi = self.bno.readAngle()
				self.ser.setfermo()
				if not self.cella_successiva:
					self.situazione = 'fine finecorsa'
				else:
					self.situazione = 0
			else:
				self.situazione = 'finecorsa'
			self.ser.setfermo()
		self.colori = 0
		########################################## FINECORSA CENTRALE #######################################################
		if self.situazione=='finecorsa':
			val = self.piastre.fermaa() 
			if (val[1] > 500) and (val[2] > 500) and (val[3] > 500 and val[3] < 3400):
				print('bluufalso')
				self.colori='blu'
				self.ser.setfermo(0)
				sleep(5)
			if self.laser.read(0)<15:
				self.ser.azzeroimpulsi()
				while (self.impulsi2 < 24):
					self.impulsi2 = self.ser.setindietro()
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.situazione=0
				self.ser.setfermo()
			if self.cella_successiva:
				self.situazione = 0
		self.impulsi2=0
		########################################## PLACCA NERA #######################################################
		if self.situazione == 'nero' or self.situazione == 'nerosalita':
			if self.situazione == 'nero':
				self.ser.clean()
				controllo = self.ser.azzeroimpulsi()
				while controllo == 'serial error':
					self.ser.clean()
					controllo = self.ser.azzeroimpulsi()
				print('fatta bro')
				print (controllo)
				target = 120
				self.impulsi2 = 0
				self.ser.setindietro()
				while (self.impulsi2 < target):
					self.ser.clean()
					self.impulsi2 = self.ser.setindietro()
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.ser.setfermo()
				sleep(0.1)
			elif self.situazione == 'nerosalita':
				self.situazione = 'nero'
		self.ser.clean()
		########################################## CONTROLLO COLORE PLACCA (BLU, ARGENTO, BIANCA) #######################################################
		pias = self.ser.piastre()
		if pias == 'serial error':
			pias = self.last_colo/3.92
		pias = pias*3.92
		#print('piastra attuale', pias)
		if pias == 'serial error':
			pias = self.last_colo
		val = self.piastre.fermaa() 
		inclina = self.bno.inclinazione()
		if (val[1] > 360) and (val[2] > 500) and (val[3] > 500 and val[3] < 3400) and self.colori!='blu' and self.situazione!='nero':
			self.colori = 'blu'
			print('bluu vero')
			self.ser.setfermo()
			sleep(5)
		elif self.last_colo > pias +80 and	(self.incliiniz-2<inclina<self.incliiniz+2) and self.situazione!='nero':
			self.colori = 'argento'
			print('argento')
		elif pias-80 < self.last_colo < pias+80 and self.situazione!='nero':
			print('bianco')
			self.last_colo = pias
			self.colori = 'bianco'
		else:
			print('rifjrok')
		########################################### POSIZIONE FINALE 30 CM ####################################################################
		'''if(self.laser.read(0) > 45 and self.laser.read(0) < 112):
			while (self.laser.read(0) > 50 and self.laser.read(0) < 112):
				self.ser.cm()
				print("ecoooooooooooooooooooooooooo")
			self.ser.setfermo()
			controllo = self.ser.azzeroimpulsi()
			while controllo == 'serial error':
				controllo = self.ser.azzeroimpulsi()
			sleep(0.1)'''
		########################################## INFORMAZIONI CHE ANDRANNO ALLA MAPPA #######################################################
		uscita = []
		if self.situazione == 'finecorsa':
			uscita.append('finecorsa')
		elif self.situazione == 'fine finecorsa':
			uscita.append('finecorsa')
		elif self.situazione == 'salita':
			uscita.append('salita')
		elif self.situazione == 'discesa':
			uscita.append('discesa')
		elif self.situazione == 'nero':
			uscita.append('nero')
		if self.colori == 'blu':
			 uscita.append('blu')
		elif self.colori == 'argento':
			uscita.append('argento')
		else:
			uscita.append(301)
		self.situazione = 0
		self.ser.setfermo()
		return uscita
		
	def check_sens(self):
		muri = []
		self.inclinazione = self.bno.inclinazione()
		if self.laser.read(0) > 140  or self.inclinazione > 20:
			muri.append("avanti")
		if self.laser.read(2) > 200 or self.laser.read(3) > 200:
			muri.append("destra")
		if self.laser.read(1) > 200 or self.laser.read(4) > 200:
			muri.append("sinistra")
		return muri

		
	def partenza(self):
		pias = 'serial error'
		while (pias == 'serial error') or (pias < 0) or (pias>1000):
			pias = self.ser.piastre()
			#print('inizio piastre ',pias)
		pias = pias*3.92
		self.last_colo = pias
	def prova(self):
		if (GPIO.input(centro) == True or GPIO.input(destra) == True or GPIO.input(sinistra) == True):  #centro destra sinistra
					print('premuto')
def get_flag():
	with open('fermo.txt', 'r') as file:
		flag = file.readline().strip()
	flag = False if flag == "False" else True
	#print('FLAG', flag)
	return flag	
			
if __name__ == '__main__':  
	mov = Movimenti()
	mov.init() 
	led = Led()
	laser = VL6180X()
	mov.bno.begin()
	mov.piastre.begin()
	sleep(1)
	mov.partenza()	
	while True:
		mov.cm30()
		sleep(2)
