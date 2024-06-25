import time
from time import sleep
import adafruit_vl6180x as vl6180
from libBNO055 import BNO055
from SERIALE import Serial
from SENS_DIST import VL6180X
from led import Led
import RPi.GPIO as GPIO
from piastre2 import APDS9960
#from pidgyro import PIDController
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
'''
GPIO.setup(13, GPIO.IN)# fc1 centro
GPIO.setup(20, GPIO.IN)# fc2 destra
GPIO.setup(26, GPIO.IN)# fc3 sinistra
GPIO.setup(16, GPIO.IN)# fc4 dietro
'''
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
		byte_fermo = self.byte_fermo = 0
		byte_avanti = self.byte_avanti = 1
		byte_destra = self.byte_destra = 5
		byte_destralenta = self.byte_destralenta = 22
		byte_sinistra = self.byte_sinistra = 6
		byte_indietro = self.byte_indietro = 2
		byte_resetimpulsi = self.byte_resetimpulsi = 33
		byte_provaa = self.byte_provaa = 34
		byte_resetimpulsi2 = self.byte_resetimpulsi2 = 35
		self.impulsi=0
		self.impulsi2=0	
		self.costante = 1300
		self.colore = 0
		self.nero = 0
		self.inclinazione  = 0
		self.impulsi = 0
		
		self.pin_digitale_1 = 27
		GPIO.setup(self.pin_digitale_destra, GPIO.OUT)
		GPIO.output(self.pin_digitale_destra, GPIO.LOW)
		
		self.pin_digitale_2 = 17
		GPIO.setup(self.pin_digitale_sinistra, GPIO.OUT)
		GPIO.output(self.pin_digitale_sinistra, GPIO.LOW)
		
		self.livello = 0
		self.ricordo = 0
		self.ser= Serial()
		self.piastre = APDS9960()
		self.bno = BNO055()
		self.led = Led()
		self.laser = VL6180X()
		self.bno.begin()
		#self.p_tempo = Process(target=tempo, args=(queue, self.impulsi))
		#self.pid = PIDController(100, 20, 0.1)
	#gyroscopio---------------------------------------------------------------------

	def update(self, process_variable):
		current_time = time.time()
		
		dt = current_time - self.last_time
		error = self.setpoint - process_variable 
		#print('ERROREEEEEEEEEE', error)
		# Gestione del reset del giroscopio a 360 gradi
		if error < -180:
			error += 360
		elif error > 180:
			error -= 360
		self.arduino = self.ser.read()
		if self.arduino == 'serial error':
			self.arduino = 0
		
		if self.ferma_cicli == False and self.arduino != 80:
			self.error_sum += error * dt
			d_error = (error - self.last_error) / dt
			output = self.Kp * error + self.Ki * self.error_sum + self.Kd * d_error
			if output>3000:
				self.error_sum = 0.0
				self.last_error = 0.0
			if output<-3000:
				self.error_sum = 0.0
				self.last_error = 0.0
			last_time = current_time
			self.last_error = error

			return output
		else:
			output = 0
			return output

	def controlpid(self, asse): 
			self.arduino = self.ser.read()
			#print('arduino :', self.arduino)
			if self.arduino == 'serial error':
				self.arduino = 0
			if self.arduino == 80:
				self.error_sum = 0.0
				self.last_error = 0.0
			if self.arduino != 80:
				# Simulazione della lettura del giroscopio
				# Nel tuo caso, dovrai leggere il valore reale dal tuo giroscopio
				gyro_value = self.bno.readAngle()
				#print('bnooooooooooo0000000    ', gyro_value)
				# Calcola l'output del controllore PID
				output = self.update(gyro_value)
				#print('output: ',output)
				# Utilizza l'output per controllare i due motori separatamente
				right_motor_speed = output
				left_motor_speed = -output
				sleep(0.1)
				return right_motor_speed, left_motor_speed
				#time.sleep(0.01)  # Attendi per un breve periodo prima di ripetere il ciclo
			else:
				right_motor_speed = 0
				left_motor_speed = 0
				#mov.dritta()
				self.ser.setfermo(0)
				return right_motor_speed, left_motor_speed
	
	
	#-------------------------------------------------------------------------------------
	def destra(self):
		z_in = self.bno.readAngle()
		self.ser.setdestra(3000)
		sleep(0.2)
		if z_in > 273.6:
			obiettivo = z_in - 273.6
			z_at = self.bno.readAngle()
			while ((z_at >= z_in) or (z_at < obiettivo)):
				flag = get_flag()
				if not flag:
					z_at = self.bno.readAngle()
					#print(z_at)
					if z_at < 0 or z_at > 360:
						z_at = z_in 
					if z_at < obiettivo-16 or 350<z_at<360:
						self.ser.setdestra(3000)
					else:
						self.ser.setdestra(1000)
				else:
					self.ser.setfermo(0)
			#print('SONO 11111111111111111111111111')
			self.ser.setfermo(0)
		else:
			obiettivo = z_in + 85.4
			z_at = self.bno.readAngle()
			while (z_at < obiettivo):
				flag = get_flag()
				if not flag:
					z_at = self.bno.readAngle()
					#print(z_at)
					if z_at < 0 or z_at > 360:
						z_at = obiettivo - 1
					if z_at > obiettivo-16:
						self.ser.setdestra(1000)
					else:
						self.ser.setdestra(3000)
				else:
					self.ser.setfermo(0)
			#print('SONO 22222222222222222222222222')
			self.ser.setfermo(0)
		print("girato a destra")
	def sinistra(self):
		#print('FLAG', flag)
		#print('sono entrato in sinistra')
			self.ser.setsinistra(3000)
			sleep(0.2)
			z_in = self.bno.readAngle()
			if z_in < 84:
				obiettivo = z_in + 276
				z_at = self.bno.readAngle()
				while ((z_at <= z_in) or (z_at > obiettivo) ):
					flag = get_flag()
					if not flag:
						z_at = self.bno.readAngle()
						#print(z_at)
						if z_at < 0 or z_at > 360:
							z_at = z_in 
						if 20<z_at<80:
							self.ser.setsinistra(3000)
						else:
							self.ser.setsinistra(1000)
					else: 
						#print('pauseeee')
						self.ser.setfermo(0)
				#print('SONO 11111111111111111111111111')
				self.ser.setfermo(0)
			else:
				obiettivo = z_in - 84
				z_at = self.bno.readAngle()
				while (z_at > obiettivo):
					flag = get_flag()
					if not flag:
						z_at = self.bno.readAngle()
						if z_at < 0 or z_at > 360:
							z_at = z_in
						if z_at<obiettivo+25:	
							self.ser.setsinistra(1000)
						else:
							self.ser.setsinistra(3000)
					else:
						#print('pauseeee')
						self.ser.setfermo(0)
				#print('SONO 22222222222222222222222222')
				self.ser.setfermo(0)
			print("girato a sinistra")

	def riposizionamento(self):
		#print('riposizionamento')
		#print('FLAG', flag)
		while (GPIO.input(dietro) == False):
			flag = get_flag()
			if not flag:
				self.ser.setindietro(2500)
				self.ser.clean()
			else:
				self.ser.setfermoflag(0)
				self.ser.clean()
		self.ser.clean()
		self.ser.setfermo(0)
		sleep(0.05)
		self.impulsi=0
		controllo = self.ser.azzeroimpulsi()
		while controllo == 'serial error':
			controllo = self.ser.azzeroimpulsi()
		print('fatta bro')
		while (self.impulsi < 30):
			self.impulsi = self.ser.setavanti(3000, 3000)
			if self.impulsi=='serial error':
				self.impulsi = 0
			#print('eccogliimpulis')
			print(self.impulsi)
			sleep(0.01)
		#print(self.impulsi)
		self.ser.clean()
		self.ser.setfermo(0)
		self.ser.setfermo(0)
		#print('fatto')
		sleep(0.1)
		
	async def first_task(self):
		self.ferma_cicli = False
		gyro_value = 0  # Valore del giroscopio
		self.setpoint = self.asse
		#print('setpoint', self.setpoint) Kp = 100 Ki = 30 Kd = 0
		Kp = 0
		Ki = 0
		Kd = 0
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.error_sum = 0.0
		self.last_error = 0.0
		self.last_time = time.time()
		impulsi_old = 0
		self.up =0
		self.right_motor_speed = 0
		self.left_motor_speed = 0
		while (self.ferma_cicli == False):
			self.right_motor_speed, self.left_motor_speed  = self.controlpid(self.asse)
			await asyncio.sleep(0.001)     
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
					#print('ecococo')
					if  (GPIO.input(destra) == True and GPIO.input(sinistra) == False):  
						self.situazione = 'finecorsa destra'
					elif  (GPIO.input(sinistra) == True and GPIO.input(destra) == False):
						self.situazione = 'finecorsa sinistra'
					else:
						self.situazione = 'finecorsa'
					self.ferma_cicli = True
			#print('VRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR',self.inclinazione)
			
			if (self.inclinazione < -15):
				self.situazione = 'salita'
				self.ferma_cicli = True
			if (self.inclinazione > 20):
				self.situazione = 'discesa'
				self.ferma_cicli = True
			
			#print('fatto')
			await asyncio.sleep(0.001)
	async def third_task(self):
		nuova_cella = True
		self.ferma_cicli = False
		self.salita = False
		self.inclinazione = self.bno.inclinazione()
		while (self.ferma_cicli == False):
			flag = get_flag()
			if not flag:
				self.ser.clean()
				imp = self.ser.setavanti(3000-self.right_motor_speed, 3000-self.left_motor_speed)
				self.right_motor_speed = 0
				self.left_motor_speed = 0
				#print(imp)
				if imp == 'serial error':
					imp = 20
				#print(imp)
				if imp > 100 and nuova_cella:    # condizione per capire in quale cella sta la vittima
					with open('valore.txt', 'r') as file:
						index_next_cell = int(file.readline().strip())
					queue.put('cella')
					queue.put(index_next_cell)
					nuova_cella = False
					self.cella_successiva = True
				if (self.inclinazione < -20):
					self.salita = True
				if imp > 230 and self.salita == False:
					self.ferma_cicli = True
					break
				if imp > 230 and self.salita == True:
					self.ferma_cicli = True
					break
				await asyncio.sleep(0.001)
			else:
				self.ser.setfermoflag(0)
		return '30cm'
		
	async def main(self):
		results = await asyncio.gather(self.first_task(), self.second_task(), self.third_task())
		self.first_task_result, self.second_task_result, self.third_task_result = results
	def partenza(self):
		pias = 'serial error'
		while pias == 'serial error':
			pias = self.ser.piastre()
			#print('inizio piastre ',pias)
		pias = pias*3.92
		self.last_colo = pias
			
	def cm30(self):
		self.dritta()
		self.situazione = 0
		self.cella_successiva = False
		self.led.led_sotto_ON()
		self.impulsi = 0	
		self.ser.azzeroimpulsi()
		sleep(0.001)
		#self.bno.begin()
		self.asse = self.bno.readAngle()
		#print('ASSSSEEEEEEE', self.asse)
		self.ferma_cicli = False
		self.ser.clean()
		while True:
			asyncio.run(self.main())
			if (self.second_task_result == 'nero') or (self.second_task_result == 'finecorsa') or (self.third_task_result == '30cm'):
				break
		self.ser.setfermo(0)
		#self.inclinazione = self.bno.inclinazione()
		if self.situazione == 'discesa':
			print("discesa")
			while (self.inclinazione>9) or (self.inclinazione<-30) or (self.inclinazione ==-0.0625):
				lettura_sinistra = self.laser.read(1)
				sleep(0.01)
				print(self.inclinazione)
				lettura_destra = self.laser.read(2)
				while lettura_sinistra<70:
					if lettura_sinistra<50:
						break
					else:
						self.ser.setavanti(3400, 2800)
					lettura_sinistra = self.laser.read(1)
					sleep(0.01)
				while lettura_destra<70:
					if lettura_destra<50:
						break
					else:
						self.ser.setavanti(2800, 3400)
					lettura_destra = self.laser.read(2)
					sleep(0.01)
				if lettura_sinistra>70 and lettura_destra>70:
					self.ser.setavanti(3000, 3000)
					lettura_destra = self.laser.read(2)
					lettura_sinistra = self.laser.read(1)
					self.ser.clean()
				sleep(0.1)
				self.inclinazione = self.bno.inclinazione()
				#print(self.inclinazione)
			GPIO.output(self.pin_digitale_destra, GPIO.LOW)
			GPIO.output(self.pin_digitale_sinistra, GPIO.LOW)
			self.impulsisd=0
			self.ser.azzeroimpulsi()
			sleep(0.1)
			#print(self.impulsisd)
			while (self.impulsisd < 70):
				self.impulsisd = self.ser.setavanti(3000, 3000)
				if self.impulsisd =='serial error':
					self.impulsisd = 0
				sleep(0.01)
		if self.situazione == 'finecorsa destra':
			if self.laser.read(0)>15:
				#print('finecorsa destra')
				self.ser.azzeroimpulsi()
				sleep(0.01)
				self.impulsi2=0
				while (self.impulsi2 < 60):
					self.impulsi2 = self.ser.setindietro(3000)
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.ser.setfermo(0)
				self.bno.begin()
				gradi = self.bno.readAngle()
				while (gradi > 340) or (0 <= gradi <= 2) or (gradi < 1) or (gradi > 361):
					self.ser.setsinistra(1000)
					gradi = self.bno.readAngle()
				self.ser.setfermo(0)
				if not self.cella_successiva:
					self.situazione = 'fine finecorsa'
				else:
					self.situazione = 0
			else:
				self.situazione = 'finecorsa'
			self.ser.setfermo(0)
		if self.situazione == 'finecorsa sinistra':
			if self.laser.read(0)>15:
				#print('finecorsa sinistra')
				self.ser.azzeroimpulsi()
				sleep(0.01)
				self.impulsi2=0
				while (self.impulsi2 < 60):
					self.impulsi2 = self.ser.setindietro(3000)
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.ser.setfermo(0)
				self.bno.begin()
				gradi = self.bno.readAngle()
				while (gradi < 20) or (358 <= gradi <= 360) or (gradi < 1) or (gradi > 361):
					self.ser.setdestra(1000)
					gradi = self.bno.readAngle()
				self.ser.setfermo(0)
				if not self.cella_successiva:
					self.situazione = 'fine finecorsa'
				else:
					self.situazione = 0
			else:
				self.situazione = 'finecorsa'
			self.ser.setfermo(0)
		self.colori = 0
		if self.situazione=='finecorsa':
			val = self.piastre.fermaa() 
			if (val[1] > 500) and (val[2] > 500) and (val[3] > 500 and val[3] < 3000):
				print('bluufalso')
				self.colori='blu'
				self.ser.setfermo(0)
				sleep(5)
			if self.laser.read(0)<15:
				self.ser.azzeroimpulsi()
				while (self.impulsi2 < 24):
					self.impulsi2 = self.ser.setindietro(3000)
					if self.impulsi2 == 'serial error':
						self.impulsi2 = 3
				self.situazione=0
				self.ser.setfermo(0)
			if self.cella_successiva:
				self.situazione = 0
		self.impulsi2=0
		if self.nero == 'nero':
			controllo = self.ser.azzeroimpulsi()
			while controllo == 'serial error':
				controllo = self.ser.azzeroimpulsi()
			print('fatta bro')
			target = 100
			self.impulsi2 = 0
			while (self.impulsi2 < target):
				self.impulsi2 = self.ser.setindietro(3000)
				#print(self.impulsi2)
				if self.impulsi2 == 'serial error':
					self.impulsi2 = 3
			self.ser.setfermo(0)
			sleep(0.1)
		self.ser.clean()
		pias = self.ser.piastre()
		if pias == 'serial error':
			pias = self.last_colo/3.92
		pias = pias*3.92
		#print('piastra attuale', pias)
		if pias == 'serial error':
			pias = self.last_colo
		val = self.piastre.fermaa() 
		inclina = self.bno.inclinazione()
		if (val[1] > 360) and (val[2] > 500) and (val[3] > 500 and val[3] < 3000) and self.colori!='blu':
			self.colori = 'blu'
			print('bluu vero')
			self.ser.setfermo(0)
			sleep(5)
		elif self.last_colo > pias +100 and	-2<inclina<2:
			self.colori = 'argento'
			print('argento')
		elif pias-100 < self.last_colo < pias+100:
			print('bianco')
			self.last_colo = pias
			self.colori = 'bianco'
		else:
			print('rifjrok')
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
		if self.situazione == 'salita':
			print("salita")
			while (self.inclinazione<-4) or (self.inclinazione ==-0.0625):
				lettura_sinistra = self.laser.read(1)
				sleep(0.01)
				lettura_destra = self.laser.read(2)
				while lettura_sinistra<70:
					if lettura_sinistra<50:
						self.ser.setavanti(3000, 3000)
						break
					else:
						self.ser.setavanti(3400, 2800)
					lettura_sinistra = self.laser.read(1)
					sleep(0.01)
				while lettura_destra<70:
					if lettura_destra<50:
						self.ser.setavanti(3000, 3000)
						break
					else:
						self.ser.setavanti(2800, 3400)
					lettura_destra = self.laser.read(2)
					sleep(0.01)
				if lettura_sinistra>70 and lettura_destra>70:
					self.ser.setavanti(3000, 3000)
					lettura_destra = self.laser.read(2)
					lettura_sinistra = self.laser.read(1)
					self.ser.clean()
				sleep(0.1)
				self.inclinazione = self.bno.inclinazione()
				#print(self.inclinazione)
		
			GPIO.output(self.pin_digitale_destra, GPIO.LOW)
			GPIO.output(self.pin_digitale_sinistra, GPIO.LOW)
			self.impulsisd=0
			if self.ricordo == 1:
				self.ricordo = 0
			else:
				self.ricordo = 1
			self.ser.azzeroimpulsi()
			sleep(0.1)
			while (self.impulsisd < 70):
				self.impulsisd = self.ser.setavanti(3000, 3000)
				if self.impulsisd== 'serial error':
					self.impulsisd=0
		print(uscita)
		self.situazione = 0
		self.ser.setfermo(0)
		return uscita


				
	def dritta(self):
			if(self.laser.read(1) < 50 and (self.laser.read(4)+9)<50):
				self.ser.setdestra(1600)
				print('ok')
				sleep(0.4)
			if(self.laser.read(2) < 50 and (self.laser.read(3))<50):
				self.ser.setdestra(1600)
				print('si33')
				sleep(0.4)	
			if(self.laser.read(1) <120 and (self.laser.read(4)+10)>70 and (self.laser.read(4)+10)<170): # sx dav, sx dietro, sx dietro
					while((self.laser.read(1)/(self.laser.read(4)+10))<0.94):
						self.ser.setdestra(600)
			self.ser.setfermo(0)
			sleep(0.01)
			
			if((self.laser.read(4)+10) <120 and self.laser.read(1)>70 and self.laser.read(1)<170): # sx dietro, sx dav, sx dav
				while((self.laser.read(4)+10)/(self.laser.read(1))<0.94):
					self.ser.setsinistra(600)
			self.ser.setfermo(0)
			sleep(0.01)
			if(self.laser.read(2) <120 and (self.laser.read(3)+12)>70 and (self.laser.read(3)+12)<170): # dx dav, dx dietro, dx dietro
				while((self.laser.read(2)/(self.laser.read(3)+12))<0.94):
					self.ser.setsinistra(600)
			self.ser.setfermo(0)
			sleep(0.01)
			if((self.laser.read(3)+12) <120 and self.laser.read(2)>70 and self.laser.read(2)<170):
				while(((self.laser.read(3)+12)/self.laser.read(2))<0.94):
					self.ser.setdestra(600)
			self.ser.setfermo(0)
			sleep(0.01)
		
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

def get_flag():
	with open('fermo.txt', 'r') as file:
		flag = file.readline().strip()
	flag = False if flag == "False" else True
	#print(flag)
	return flag	
'''
def set_flag(value):
	global fermo
	fermo = value	

def get_flag():
	return fermo
'''	
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
		print('prima')
		mov.cm30()
		sleep(1)
		'''
		if laser.read(0)<150:
			mov.destra()
		if laser.read(5)<120:
			mov.riposizionamento()
		mov.cm30()
		sleep(0.1)
		'''
		'''
		mov.cm30()
		t0 = time.time()
		while True:
			mov.ser.setfermo(0)
			t1 = time.time()
			timeRunning = t1 - t0
			if timeRunning >= 5:
				print('finia la pausa')
				break
		mov.cm30()
		'''
