import json, rpc, serial, serial.tools.list_ports, struct, sys
import RPi.GPIO as GPIO
from datetime import datetime

'''
print("\nAvailable Ports:\n")
for port, desc, hwid in serial.tools.list_ports.comports():
	print("{} : {} [{}]".format(port, desc, hwid))
sys.stdout.write("\nPlease enter a port name: ")
sys.stdout.flush()
interface = rpc.rpc_usb_vcp_master(port=input())
print("")
sys.stdout.flush()
'''
print("\nAvailable Ports:\n")
available_ports = list(serial.tools.list_ports.comports())
print(available_ports)
print("\n")
if not available_ports:
	print("No serial ports found. Exiting.")
	sys.exit()

# Select the first available port automatically
selected_port1 = available_ports[0][0]
selected_port2 = available_ports[1][0]
# print(selected_port1, selected_port2)
print("\n")
print("Selected Port: {} [{}]".format(selected_port1, available_ports[0][2]))
# print("Selected Port: {} [{}]".format(selected_port2, avai lable_ports[1][2]))
# Initialize RPC interface with the selected port
interface1 = rpc.rpc_usb_vcp_master(port=selected_port1)
interface2 = rpc.rpc_usb_vcp_master(port=selected_port2)
print("")
sys.stdout.flush()


def exe_color_detection():
	try:
		result1 = interface1.call("color_detection")  # sinistra
		result2 = interface2.call("color_detection")  # destra
	except:
		print('colore errore')
		result1 = None
		result2 = None		
	if result1 is not None and result2 is not None:
		colore1 = struct.unpack("5s", result1)[0].decode('utf-8')
		colore2 = struct.unpack("5s", result2)[0].decode('utf-8')
		if (colore2 == 'giall'): #sinistra giallo
			lettera_s=1
		elif(colore2 == 'rosso'): #sinistra rosso
			lettera_s=2
		elif(colore2 == 'verde'): #sinistra verde
			lettera_s=3
		else:
			lettera_s = 40
		if(colore1 == 'giall'): #destra giallo
			lettera_d=4
		elif(colore1 == 'rosso'): #destra rosso
			lettera_d=5
		elif(colore1 == 'verde'): #destra verde
			lettera_d=6
		else:
			lettera_d = 40		
	else:
		lettera_s = 40
		lettera_d = 40
	return lettera_s, lettera_d


def exe_letter_detection():
	try:
		result1 = interface1.call("letter_detection")
		result2 = interface2.call("letter_detection")
	except:
		print('lettere errore')
		result1 = None
		result2 = None
	if result1 is not None and result2 is not None:
		value1 = struct.unpack("9sf", result1)
		value2 = struct.unpack("9sf", result2)
		letter_d = value1[0].decode('utf-8')
		letter_s  = value2[0].decode('utf-8')
		#print(letter_s, letter_d)
		if letter_s == 'lettera_U' and value2[1] > 0.95:  # sinistra
			letter_s = 7
		elif letter_s == 'lettera_H' and value2[1] > 0.95:  # sinistra
			letter_s = 8
		elif letter_s == 'lettera_S' and value2[1] > 0.95:  # sinistra
			letter_s = 9
		else:
			letter_s = 40
		if letter_d == 'lettera_U' and value1[1] > 0.95:  # destra
			letter_d = 10
		elif letter_d == 'lettera_H' and value1[1] > 0.95:  # destra
			letter_d = 11
		elif letter_d == 'lettera_S' and value1[1] > 0.95:  # destra
			letter_d = 12
		else:
			letter_d = 40
		return letter_s, value2[1], letter_d, value1[1]
	else:
		return 40, 0, 40, 0


def exe_placche_detection():
	try:
		result1 = interface1.call("placche_detection")
		result2 = interface2.call("placche_detection")
	except:
		print('placche errore')
		result1 = None
		result2 = None
	if result1 is not None and result2 is not None:
		placche1 = struct.unpack("2s", result1)[0].decode('utf-8')
		placche2 = struct.unpack("2s", result2)[0].decode('utf-8')
		return placche1, placche2
	else:
		return "no", "no"

def exe_led(lato, victim):
	#if lato == 'DESTRA':
	#	result1 = interface1.call("led_blink", struct.pack("5s", victim.encode('utf-8')))
	#elif lato == "SINISTRA":
	#	result2 = interface2.call("led_blink", struct.pack("5s", victim.encode('utf-8')))
	
	'''
	if result is not None:
		value = struct.unpack("5s", result)
		value = value[0].decode('utf-8')
		print(value)
	'''

if __name__ == '__main__':
	while True:
		
		#exe_color_detection()
		colore_s, colore_d = exe_color_detection()
		print(colore_s, colore_d)
		
		if colore_d == 40 and colore_s == 40:
			lettera_s, value_s, lettera_d, value_d = exe_letter_detection()
			print('DESTRA', lettera_d, value_d)
			print('SINISTRA', lettera_s, value_s)
		'''
		if colore_d != "nulla":
			exe_led("DESTRA", colore_d)
		if colore_s != "nulla":
			exe_led("SINISTRA", colore_s)
		'''
		placche_d, placche_s = exe_placche_detection()
		print(placche_d, placche_s)
		'''
		if placche_d == "si":
			exe_led("DESTRA", "placc")
		elif placche_s == "si":
			exe_led("SINISTRA", "placc")
		'''
