import pygame
from baila import Movimenti, queue
import RPi.GPIO as GPIO
import nuove_camere 
from nuove_camere import videocamere 
from led_7 import Led
from multiprocessing import Process, Queue, Value, Array
import time
from time import sleep
from servo_7 import Servo
import subprocess
from colorama import Fore, Back, Style
from SENS_DIST_7 import VL6180X
import signal
from outro2_7 import outro
import cv2
subprocess.call('sudo pigpiod', shell=True)
sleep(0.1)



RES = WIDTH, HEIGHT = 842, 842
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE
mov = Movimenti()
led = Led()
servo = Servo()
servo.init()
mov.init()
start = 0
Pin_errore = 12
cam = videocamere()
outro = outro()
mov.piastre.begin()


class Cell:
	import RPi.GPIO as GPIO
	def __init__(self, x, y):
		self.x, self.y = x, y
		self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
		self.visited = False
		self.thickness = 4
		self.colore = {'rosso': {'rosso_s' : Value('b', False), 'rosso_d' : Value('b', False)},
						 'giallo': {'giallo_s' : Value('b', False), 'giallo_d' : Value('b', False)},
						 'verde': {'verde_s': Value('b', False), 'verde_d': Value('b', False)}}
		self.lettere = { 'h': {'h_s' : Value('b', False), 'h_d' : Value('b', False)},
						 's': {'s_s' : Value('b', False), 's_d' : Value('b', False)},
						 'u': {'u_s': Value('b', False), 'u_d': Value('b', False)}}
		self.coo_v = Array('i', 2) 
		self.placca = {'blu': False, 'argento': False, 'nero': False, 'objective': False, 'dislivello': False}
		self.condizioni_esterne = {'salita': False, 'ostacolo': False} 
		
		
	def draw(self):
		x, y = self.x * TILE, self.y * TILE
		if self.visited:
			pygame.draw.rect(sc, pygame.Color('antiquewhite'), (x, y, TILE, TILE))

		if self.walls['top']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
		if self.walls['right']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
		if self.walls['bottom']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
		if self.walls['left']:
			pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)
		if self.condizioni_esterne['salita']:
			pygame.draw.rect(sc, pygame.Color('white'), (x, y, TILE, TILE))

		# PLACCHE
		if self.placca['objective']:
			pygame.draw.rect(sc, pygame.Color('purple'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['nero']:
			pygame.draw.rect(sc, pygame.Color('black'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['argento']:
			pygame.draw.rect(sc, pygame.Color('grey'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['blu']:
			pygame.draw.rect(sc, pygame.Color('blue'), (x + 2, y + 2, TILE - 2, TILE - 2))
		if self.placca['dislivello']:
			pygame.draw.rect(sc, pygame.Color('tan'), (x + 2, y + 2, TILE - 1, TILE - 1))

		# COLORI
		if bool(self.colore['rosso']['rosso_s'].value):
			pygame.draw.rect(sc, pygame.Color('red'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['rosso']['rosso_d'].value):
			pygame.draw.rect(sc, pygame.Color('red'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['giallo']['giallo_s'].value):
			pygame.draw.rect(sc, pygame.Color('gold'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['giallo']['giallo_d'].value):
			#print(self.coo_v, grid_cells.index(self))
			pygame.draw.rect(sc, pygame.Color('gold'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['verde']['verde_s'].value):
			pygame.draw.rect(sc, pygame.Color('green'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))
		if bool(self.colore['verde']['verde_d'].value):
			pygame.draw.rect(sc, pygame.Color('green'), (self.coo_v[0], self.coo_v[1], TILE/10, TILE/10))

		# LETTERE
		if bool(self.lettere['h']['h_s'].value):
			text = font.render("H", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['h']['h_d'].value):
			text = font.render("H", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['s']['s_s'].value):
			text = font.render("S", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['s']['s_d'].value):
			text = font.render("S", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['u']['u_s'].value):
			text = font.render("U", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)
		if bool(self.lettere['u']['u_d'].value):
			text = font.render("U", True, (0,0,0,1))
			text_rect = text.get_rect()
			text_rect.center = (self.coo_v[0], self.coo_v[1])
			sc.blit(text, text_rect)

	def new_cell(self, muoviamoci, posizione):
		index = grid_cells.index(self)
		movimento = muoviamoci[0] 
		next_cell = current_cell
		mossa = 0
		if movimento == 'avanti':
			if posizione == 90:
				next_cell = grid_cells[index - 1]
			elif posizione == 270:
				next_cell = grid_cells[index + 1]
			elif posizione == 0:
				next_cell = grid_cells[index - cols]
			elif posizione == 180:
				next_cell = grid_cells[index + cols]
			with open('valore.txt', 'w') as file:
				file.write(str(grid_cells.index(next_cell)))
			while True:		
				#GPIO.output(Pin_errore, GPIO.HIGH)
				mossa = mov.cm30()
				mov.dritta()
				break
			print('FINE AVANTI')
		elif movimento == 'gira a destra':
			if posizione == 90:
				posizione = 0
			elif posizione == 270:
				posizione = 180
			elif posizione == 0:
				posizione = 270
			elif posizione == 180:
				posizione = 90
			queue.put('posizione')
			queue.put(posizione)
			while True:
				#GPIO.output(Pin_errore, GPIO.HIGH)
				mossa = mov.destra()
				if muoviamoci[1]!='gira a destra' and mov.laser.read(5)<120 and mov.laser.read(3)>220 and mov.laser.read(4)>220:  # no len perchè dopo destra sempre altro
					mov.riposizionamento()
				else:
					mov.dritta()
				break
		elif movimento == 'gira a sinistra':
			if posizione == 90:
				posizione = 180
			elif posizione == 270:
				posizione = 0
			elif posizione == 0:
				posizione = 90
			elif posizione == 180:
				posizione = 270
			queue.put('posizione')
			queue.put(posizione)
			while True:		
				#GPIO.output(Pin_errore, GPIO.HIGH)
				mossa = mov.sinistra()
				if mov.laser.read(5)<130 and mov.laser.read(3)>220:
					mov.riposizionamento()
				else:
					mov.dritta()
				break
		
		return next_cell, posizione, mossa	
			
	def check_cell(self, x, y):
		find_index = lambda x, y: x + y * cols
		if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
			return False
		return grid_cells[find_index(x, y)]

	def create_dict(self, cells):
		shortest_cell_path = []
		visitable_cell = []
		if cells == None:
			for cell in grid_cells:
				if not cell.visited and not all(cell.walls.values()):
					visitable_cell.append(cell)
			if len(visitable_cell) == 0:
				target = grid_cells[int((cols*rows)/2)]
				visitable_cell.append(target)
		else:
			visitable_cell = cells
		#print('DICT', grid_cells.index(self))
		for target in visitable_cell:
			#print('TARGET', grid_cells.index(target))
			fwdPath = []
			unvisited = {n: float('inf') for n in grid_cells}  # valore infinito positivo
			unvisited[self] = 0  # costo cela iniziale 0
			visited = {}
			revPath = {}
			while unvisited:  # go until unvisited is empty
				currCell = min(unvisited, key=unvisited.get)  # prendi la cella col minimo costo dal dictionary
				# print(grid_cells.index(currCell))
				visited[currCell] = unvisited[currCell]  # add the cell to the dictionary
				if currCell == target:
					break
				for wall in currCell.walls:
					if not currCell.walls[wall]:  # se non c'è il muro
						if wall == 'top':
							childCell = currCell.check_cell(currCell.x, currCell.y - 1)
						elif wall == 'right':
							childCell = currCell.check_cell(currCell.x + 1, currCell.y)
						elif wall == 'bottom':
							childCell = currCell.check_cell(currCell.x, currCell.y + 1)
						elif wall == 'left':
							childCell = currCell.check_cell(currCell.x - 1, currCell.y)
						if childCell in visited:  # se è già presente vai alla prossima (per i vicoli cieci)
							continue
						tempDist = unvisited[currCell] + 1  # assume il numero più corto per raggiungere la casella
						if tempDist < unvisited[childCell]:
							unvisited[childCell] = tempDist  # costo della cella non è più infinito
							if childCell.placca['nero']:
								unvisited[childCell] += 9999
							elif childCell.placca['blu']:
								unvisited[childCell] += 3
							revPath[childCell] = currCell
				unvisited.pop(currCell)
			cell = target  # target
			#print('fwd', grid_cells.index(cell))
			fwdPath.append(cell)
			#print(revPath)
			while cell != self:
				fwdPath.append(revPath[cell])
				cell = revPath[cell]
			fwdPath.reverse()
			if len(shortest_cell_path) == 0 or len(fwdPath) < len(shortest_cell_path):
				shortest_cell_path = fwdPath
		mostra_sentiero = True
		#for cell in shortest_cell_path:
			#print(grid_cells.index(cell))
		cell_before = shortest_cell_path[0]
		posizione_dij = posizione
		muoviamoci = []
		while mostra_sentiero:
			for cell in shortest_cell_path:
				draw_base()
				#pygame.draw.rect(sc, pygame.Color('purple'), (cell.x * TILE, cell.y * TILE, TILE, TILE - 1))
				posizione_dij, muoviamoci = define_posizione(cell_before, cell, posizione_dij, muoviamoci)
				draw_robot(posizione, x_robot, y_robot)
				pygame.display.flip()
				cell_before = cell
				clock.tick(10)
			mostra_sentiero = False
		return shortest_cell_path, muoviamoci # might just need the last cell
		
	def destroy_wall(self, posizione, muri):  # could be done with conditions for each wall
		#cell_destra = [10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120]
		cell_destra = [18, 37, 56, 75, 94, 113, 132, 151, 170, 189] # da cambiare se cambiano rows or cols
		index = grid_cells.index(self)
		for muro in muri:  # muri = ['avanti', ...]
			if muro == 'avanti':
				if posizione == 0 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
				elif posizione == 270 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False
				elif posizione == 180 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
				elif posizione == 90 and index % rows != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
			elif muro == 'destra':
				if posizione == 0 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False
				elif posizione == 270 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
				elif posizione == 180 and index % rows != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
				elif posizione == 90 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
			elif muro == 'sinistra':
				if posizione == 0 and index % rows != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
				elif posizione == 270 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
				elif posizione == 180 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False
				elif posizione == 90 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
			elif muro == 'dietro':
				if posizione == 0 and index < len(grid_cells) - rows:
					self.walls['bottom'] = False
					grid_cells[index + rows].walls['top'] = False
				elif posizione == 270 and index % rows != 0:
					self.walls['left'] = False
					grid_cells[index - 1].walls['right'] = False
				elif posizione == 180 and index > rows - 1:
					self.walls['top'] = False
					grid_cells[index - rows].walls['bottom'] = False
				elif posizione == 90 and not index in cell_destra:
					self.walls['right'] = False
					grid_cells[index + 1].walls['left'] = False

	def define_coo(self, posizione, verso, vittima):
		x, y = self.x * TILE, self.y * TILE
		if vittima == 'lettera':
			if (posizione == 0 and verso == 'sinistra') or (posizione == 180 and verso == 'destra'):
				x = x + TILE/7 + 3
				y = y + TILE/2
			elif (posizione == 0 and verso == 'destra') or (posizione == 180 and verso == 'sinistra'):
				x = x + TILE - TILE/7
				y = y + TILE/2
			elif (posizione == 90 and verso == 'sinistra') or (posizione == 270 and verso == 'destra'):
				x = x + TILE/2
				y = y + TILE - TILE/7
			elif (posizione == 90 and verso == 'destra') or (posizione == 270 and verso == 'sinistra'):
				x = x + TILE/2
				y = y + TILE/7 + 3
		elif vittima == 'colore':
			if (posizione == 0 and verso == 'sinistra') or (posizione == 180 and verso == 'destra'):
				x = x + 3
				y = y + TILE/2 - TILE/20
			elif (posizione == 0 and verso == 'destra') or (posizione == 180 and verso == 'sinistra'):
				x = x + TILE - TILE/10 - 1
				y = y + TILE/2 - TILE/20  # 45
			elif (posizione == 90 and verso == 'sinistra') or (posizione == 270 and verso == 'destra'):
				x = x + TILE/2 - TILE/20  # 45
				y = y + TILE - TILE/10 - 1
			elif (posizione == 90 and verso == 'destra') or (posizione == 270 and verso == 'sinistra'):
				x = x + TILE/2 - TILE/20
				y = y + 3
		return int(x), int(y)   #might need int
		
	def vittima(self, vittima_s, vittima_d, posizione, before_cell):
		#print(bool(grid_cells[5].colore['giallo']['giallo_d'].value))
		#print('UAUAU', grid_cells.index(before_cell), grid_cells.index(self))
		trovato = False	
		if not self.placca['nero']:	 # no vittime nella placca nera
			if vittima_s >= 7 and vittima_s <= 9 and self.coo_v[0] == 0 and before_cell.ultima_vittima(vittima_s):
				trovato = True
				self.coo_v[0] = self.define_coo(posizione, 'sinistra', 'lettera')[0]
				self.coo_v[1] = self.define_coo(posizione, 'sinistra', 'lettera')[1]
				with open('fermo.txt', 'w') as file:
					file.write(str(True))
				if vittima_s == 7:
					self.lettere['u']['u_s'].value = not self.lettere['u']['u_s'].value
					servo.U_sinistra()
				elif vittima_s == 8:
					self.lettere['h']['h_s'].value = not self.lettere['h']['h_s'].value
					servo.H_sinistra()
				elif vittima_s == 9:
					self.lettere['s']['s_s'].value = not self.lettere['s']['s_s'].value
					servo.S_sinistra()
				with open('fermo.txt', 'w') as file:
					file.write(str(False))
			elif vittima_d >= 10 and vittima_d <= 12 and self.coo_v[0] == 0 and before_cell.ultima_vittima(vittima_d):
				trovato = True
				self.coo_v[0] = self.define_coo(posizione, 'destra', 'lettera')[0]
				self.coo_v[1] = self.define_coo(posizione, 'destra', 'lettera')[1]
				with open('fermo.txt', 'w') as file:
					file.write(str(True))
				if vittima_d == 10:
					self.lettere['u']['u_d'].value = not self.lettere['u']['u_d'].value
					servo.U_destra()
				elif vittima_d == 11:
					self.lettere['h']['h_d'].value = not self.lettere['h']['h_d'].value
					servo.H_destra()
				elif vittima_d == 12:
					self.lettere['s']['s_d'].value = not self.lettere['s']['s_d'].value
					servo.S_destra()
				with open('fermo.txt', 'w') as file:
					file.write(str(False))
			elif vittima_s >= 1 and vittima_s <= 3 and self.coo_v[0]== 0 and before_cell.ultima_vittima(vittima_s):
				print(posizione, self.walls, grid_cells.index(self))
				self.coo_v[0] = self.define_coo(posizione, 'sinistra', 'colore')[0]
				self.coo_v[1] = self.define_coo(posizione, 'sinistra', 'colore')[1] 
				with open('fermo.txt', 'w') as file:
					file.write(str(True))
				if vittima_s == 1:
					self.colore['giallo']['giallo_s'].value = not self.colore['giallo']['giallo_s'].value
					servo.giallo_sinistra()
				elif vittima_s == 2:
					self.colore['rosso']['rosso_s'].value = not self.colore['rosso']['rosso_s'].value
					servo.rosso_sinistra()
				elif vittima_s == 3:
					self.colore['verde']['verde_s'].value = not self.colore['verde']['verde_s'].value
					servo.verde_sinistra()
				with open('fermo.txt', 'w') as file:
					file.write(str(False))
			elif vittima_d >= 4 and vittima_d <= 6 and self.coo_v[0]== 0 and before_cell.ultima_vittima(vittima_d):
				self.coo_v[0] = self.define_coo(posizione, 'destra', 'colore')[0]
				self.coo_v[1] = self.define_coo(posizione, 'destra', 'colore')[1]
				with open('fermo.txt', 'w') as file:
					file.write(str(True))
				if vittima_d == 4:
					self.colore['giallo']['giallo_d'].value = not self.colore['giallo']['giallo_d'].value
					servo.giallo_destra()
				elif vittima_d == 5:
					self.colore['rosso']['rosso_d'].value = not self.colore['rosso']['rosso_d'].value
					servo.rosso_destra()
				elif vittima_d == 6:
					self.colore['verde']['verde_d'].value = not self.colore['verde']['verde_d'].value
					servo.verde_destra()
				with open('fermo.txt', 'w') as file:
					file.write(str(False))
		return trovato
		
	def ultima_vittima(self, v):  # per controllare che la cella precedente non abbia la stessa vittima 
		#print('ultima_vittima', grid_cells.index(self))
		if (v == 1 or v == 4) and (bool(self.colore['giallo']['giallo_s'].value) or bool(self.colore['giallo']['giallo_d'].value)):
			return False 
		elif (v == 2 or v == 5) and (bool(self.colore['rosso']['rosso_s'].value) or bool(self.colore['rosso']['rosso_d'].value)):
			#print('kek')
			return False
		elif (v == 3 or v == 6) and (bool(self.colore['verde']['verde_s'].value) or bool(self.colore['verde']['verde_d'].value)):
			return False
		elif (v == 7 or v == 10) and (bool(self.lettere['u']['u_s'].value) or bool(self.lettere['u']['u_d'].value)):
			return False
		elif (v == 8 or v == 11) and (bool(self.lettere['h']['h_s'].value) or bool(self.lettere['h']['h_d'].value)):
			return False
		elif (v == 9 or v == 12) and (bool(self.lettere['s']['s_s'].value) or bool(self.lettere['s']['s_d'].value)):
			return False 
		else:
			return True
	
def camere(queue):
	last_c = centre
	last_p = 0
	last_b = centre
	current_cell = grid_cells[centre]
	while True:
		if queue.empty():
			current_cell = grid_cells[last_c]
			posizione = last_p
			before_cell = grid_cells[last_b]
		else:
			identificate = queue.get()
			i = queue.get()
			print(identificate, i)
			if identificate == 'cella':
				if last_c != i:
					before_cell = current_cell
					last_b = grid_cells.index(before_cell)
					current_cell = grid_cells[i]
					last_c = i
				else:
					current_cell = grid_cells[last_c]
					before_cell = grid_cells[last_b]
				posizione = last_p
			elif identificate == 'posizione':
				posizione = i
				last_p = i
				current_cell = grid_cells[last_c]
				before_cell = grid_cells[last_b]
			
		img, img1 = cam.telecamere()		
		#plus90_img = cv2.warpAffine(img, rotation_matrix_plus90, (width, height))
		#plus90_img1 = cv2.warpAffine(img1, rotation_matrix_plus90, (width, height))
		#plus45_img = cv2.warpAffine(img, rotation_matrix_plus45, (width, height))
		#plus45_img1 = cv2.warpAffine(img1, rotation_matrix_plus45, (width, height))
		lettera = cam.get_letter(img, 'destra')
		lettera1 = cam.get_letter(img1, 'sinistra')
		#print(lettera, lettera1)
		trovato = current_cell.vittima(lettera1, lettera, posizione, before_cell)
		'''
		if not trovato:
			lettera = cam.get_letter(plus90_img, 'destra')
			lettera1 = cam.get_letter(plus90_img1, 'sinistra')
			trovato = current_cell.vittima(lettera1, lettera, posizione, before_cell)
			if not trovato:
				lettera = cam.get_letter(plus45_img, 'destra')
				lettera1 = cam.get_letter(plus45_img1, 'sinistra')
				trovato = current_cell.vittima(lettera1, lettera, posizione, before_cell)
				'''
		if not trovato:
			color = cam.get_color(img, 'destra')
			color1 = cam.get_color(img1, 'sinistra')
			trovato = current_cell.vittima(color1, color, posizione, before_cell)
			#print('colori', color, color1)

def define_posizione(cell_before, cell, posizione_dij, muoviamoci):
	index_before = grid_cells.index(cell_before)
	index_cell = grid_cells.index(cell)
	i = index_cell - index_before
	#print(index_cell, index_before, posizione_dij)
	if posizione_dij == 0:
		if i == - rows and not cell.placca['dislivello']:
			muoviamoci.append('avanti')
		elif i == 1:
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 270
		elif i == - 1:
			muoviamoci.append('gira a sinistra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 90
		elif i == rows:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 180
	elif posizione_dij == 90:   # <--
		if i == - 1 and not cell.placca['dislivello']:
			muoviamoci.append('avanti')
		elif i == - rows:
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 0
		elif i == rows:
			muoviamoci.append('gira a sinistra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 180
		elif i == 1:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 270
	elif posizione_dij == 270:  # -->
		if i == 1 and not cell.placca['dislivello']:
			muoviamoci.append('avanti')
		elif i == rows:
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 180
		elif i == - rows:
			muoviamoci.append('gira a sinistra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 0
		elif i == -1:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 90
	elif posizione_dij == 180:
		if i == rows and not cell.placca['dislivello']:
			muoviamoci.append('avanti')
		elif i == - 1:
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 90
		elif i == 1:
			muoviamoci.append('gira a sinistra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 270
		elif i == -rows:
			muoviamoci.append('gira a destra')
			muoviamoci.append('gira a destra')
			if not cell.placca['dislivello']:
				muoviamoci.append('avanti')
			posizione_dij = 0
	return posizione_dij, muoviamoci

		
def draw_robot(posizione, x, y):
	x = int(x * TILE + 11) # da cambiare se cambiano rows or cols
	y = int(y * TILE + 11) # da cambiare se cambiano rows or cols
	if posizione == 0:
		sc.blit(robot_img, (x, y))
	elif posizione == 90:
		robot_img_sinistra = pygame.transform.rotate(robot_img, 90)  # rotate
		sc.blit(robot_img_sinistra, (x, y))
	elif posizione == 180:
		robot_img_sinistra = pygame.transform.rotate(robot_img, 180)  # rotate
		sc.blit(robot_img_sinistra, (x, y))
	elif posizione == 270:
		robot_img_sinistra = pygame.transform.rotate(robot_img, 270)  # rotate
		sc.blit(robot_img_sinistra, (x, y))


def draw_base():
	sc.fill(pygame.Color('darkslategray'))
	[cell.draw() for cell in grid_cells]

'''	
def closing(signum, frame):
	print("Chiusura dello script...")
	led.led_cam_OFF()

signal.signal(signal.SIGINT, closing)
'''	
pygame.init()
sc = pygame.display.set_mode(RES)  # window
clock = pygame.time.Clock()
robot_img = pygame.image.load(
	"/home/sensaschei2/Desktop/codici_macc_nuova/robot.png").convert()  # ottenere l'immagine
# resize
width = robot_img.get_rect().width
height = robot_img.get_rect().height
robot_img = pygame.transform.scale(robot_img, (TILE - 20, TILE - 20))  # da cambiare se cambiano rows or cols

posizione = 0
font = pygame.font.Font('freesansbold.ttf', 17)

global grid_cells
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
global centre
centre = int(cols * rows/2)
current_cell = grid_cells[centre]

height_img, width_img = 240, 320
center_img = (width_img / 2, height_img / 2)
global rotation_matrix_plus90
rotation_matrix_plus90 = cv2.getRotationMatrix2D(center_img, 90, 1.0)
global rotation_matrix_plus45
rotation_matrix_plus45 = cv2.getRotationMatrix2D(center_img, -45, 1.0)
'''
global rotation_matrix_plus90
global rotation_matrix_180
rotation_matrix_minus90 = cv2.getRotationMatrix2D(center_img, -90, 1.0)
rotation_matrix_plus90 = cv2.getRotationMatrix2D(center_img, 90, 1.0)
rotation_matrix_180 = cv2.getRotationMatrix2D(center_img, 180, 1.0)
'''
checkpoint = current_cell 
next_cell = current_cell
x_robot, y_robot = current_cell.x, current_cell.y
objective = current_cell
muoviamoci = []
check = []
celle_lack = []
togli_muro = True
before_cell = current_cell
accendere_led = True
back = True				
if __name__ == '__main__':
	#queue = Queue()
	with open('fermo.txt', 'w') as file:
		file.write(str(False))
	queue.put('cella')
	queue.put(grid_cells.index(current_cell)) 
	queue.put('posizione')
	queue.put(posizione)      
	p_cam = Process(target=camere, args=(queue, ))      
	p_cam.start()
	pin_digitale = 27
	start = 23
	lack = 24
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_digitale, GPIO.OUT)
	GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setwarnings(False)
	GPIO.output(pin_digitale, GPIO.LOW)
	mov.partenza()
	while True:
		with open('fermo.txt', 'r') as file:
			flag = file.readline().strip()
		flag = False if flag == "False" else True
		if accendere_led and not flag:
			led.led_cam_ON()
		x_robot, y_robot = current_cell.x, current_cell.y
		current_cell.visited = True
		draw_base()
		draw_robot(posizione, x_robot, y_robot)
		#print(GPIO.input(start), back) 
		if (GPIO.input(start) == True) and not flag:
			back = True
			if len(muoviamoci) != 0:
				next_cell, posizione, array_cond = current_cell.new_cell(muoviamoci, posizione)			
				print('CONDIZIONE', array_cond)
				if next_cell != current_cell and next_cell != checkpoint and not next_cell.placca['argento']:
					celle_lack.append(next_cell)
				elif next_cell == checkpoint:  # nel caso passasse nella cella iniziale
					#print('qua')
					celle_lack.clear()
				if array_cond != None:  # caso in cui gira a dx o sx
					for condizione in array_cond:
						if condizione == 'nero':
							next_cell.visited = True
							next_cell.placca['nero'] = True
							next_cell.posizione = posizione 
							objective = current_cell
							next_cell = current_cell  # rimango sulla stessa cell
						elif condizione == 'blu':
							next_cell.visited = True
							next_cell.placca['blu'] = True
						elif condizione == 'argento':
							next_cell.visited = True
							next_cell.placca['argento'] = True
							checkpoint = next_cell
							celle_lack.clear()
						elif condizione == 'discesa' or condizione == 'salita':
							print('cella salita?', grid_cells.index(next_cell))
							next_cell.visited = True
							next_cell.placca['dislivello'] = True
							i = grid_cells.index(next_cell)  # number in grid of dislivello
							next_cell.destroy_wall(posizione, ['avanti'])
							if posizione == 0:
								next_cell = grid_cells[i - rows]
							elif posizione == 90:
								next_cell = grid_cells[i - 1]
							elif posizione == 180:
								next_cell = grid_cells[i + rows]
							elif posizione == 270:
								next_cell = grid_cells[i + 1]
							print('cella successiva?', grid_cells.index(next_cell))
							celle_lack.append(next_cell)  #aggiungo quella cella lì
							if objective == grid_cells[i]:  # se l'obiettivo è la cella dello dislivello
								objective = next_cell  # obiettivo diventa la cella successiva
						elif condizione == 'finecorsa':
							next_cell = current_cell
							if next_cell in celle_lack:
								celle_lack.remove(next_cell)
							muoviamoci.insert(0, 'avanti')	
							print('finecorsaaaa', muoviamoci)
					#print(grid_cells.index(next_cell), next_cell.walls, grid_cells.index(objective))		
				muoviamoci.pop(0)
				togli_muro = True
				
			else: 
				if togli_muro:
					for i in range (0, 3):
						check = mov.check_sens()
					print(check)
					togli_muro = False	
					#print(grid_cells.index(current_cell))
				for muro in check:
					current_cell.destroy_wall(posizione, [muro])
			if objective == current_cell:
				objective.placca['objective'] = False
				path, muoviamoci = current_cell.create_dict(None)
				print('MUOVIAMOCI', muoviamoci)
				objective = path[-1]
				objective.placca['objective'] = True
				if len(muoviamoci) == 0:
					led.led_cam_OFF()
					accendere_led = False
					outro.play(outro.underworld_melody, outro.underworld_tempo, 1.3, 0.800)	
			current_cell = next_cell
			#print(GPIO.input(start), back) 
		elif (GPIO.input(start) == False) and back and len(celle_lack) > 0:   # LACK
			current_cell = checkpoint
			posizione = 0
			cells_dik = []
			#print(len(celle_lack))
			if len(celle_lack) == 1:
				lack_dik = celle_lack[-1]
				cells_dik.append(lack_dik)
			else:
				pen_cel = celle_lack[-2]
				ult_cel = celle_lack[-1]
				cells_dik.append(pen_cel)
				cells_dik.append(ult_cel)  # nel ritornare indietro magari
			path, _ = current_cell.create_dict(cells_dik)
			for cella in cells_dik:
				cella.visited = False
				cella.walls = {key: True for key in cella.walls}
				for inner_dict in cella.colore:
					for object in cella.colore[inner_dict]:
						cella.colore[inner_dict][object].value = False
				for inner_dict in cella.lettere:
					for object in cella.lettere[inner_dict]:
						cella.lettere[inner_dict][object].value = False
				cella.coo_v[0] = 0
				cella.coo_v[1] = 0
				cella.placca = {key: False for key in cella.placca}
				cella.condizioni_esterne = {key: False for key in cella.condizioni_esterne}
				i = grid_cells.index(cella)
				for wall in cella.walls:
					if wall == 'top':
						grid_cells[i - rows].walls['bottom'] = True
					if wall == 'bottom':
						grid_cells[i + rows].walls['top'] = True
					if wall == 'left':
						grid_cells[i - 1].walls['right'] = True
					if wall == 'right':
						grid_cells[i + 1].walls['left'] = True
			print(len(path))
			i_clean = grid_cells.index(path[-1])
			i_main = grid_cells.index(path[-2])
			cond = i_main - i_clean
			if cond == 1:
				path[-1].destroy_wall(0, ['destra'])
			elif cond == -1:
				path[-1].destroy_wall(0, ['sinistra'])
			elif cond == -cols:
				path[-1].destroy_wall(0, ['avanti'])
			elif cond == cols:
				path[-1].destroy_wall(0, ['dietro'])
			objective.placca['objective'] = False  # togliere il viola nel caso l'objective non fosee ancora stato visto 
			celle_lack.clear()
			muoviamoci.clear()
			objective = current_cell
			next_cell = current_cell
			togli_muro = True
			back = False
				
		pygame.display.flip()
		clock.tick(60)
