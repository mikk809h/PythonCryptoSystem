import json
import socket
import getpass
import datetime
import os
from Helpers import Debug

# Nuværende socket
sock = None
# Handshake id
client_id = None
# Er klienten logget ind?
logged_in = False

# Forbind til socket med adresse og port
server_address = ('localhost', 88)

'''
Forbind og opret socket
'''
def CreateSocket():
	# Opret TCP/IP socket
	global sock # Reference til den globale socket
	print('Forbinder til %s på port %s' % server_address)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Laver en socket
	try:
		sock.connect(server_address) # Forbinder til serveren gennem socket
	except Exception as e:
		sock = None
		print(e)

'''
Registrering
'''
def Register():
	username = input("Enter username: ")
	password = getpass.getpass("Enter password: ")

	try:
		CreateSocket()
		if not sock:
			return None

		# Definér json object
		data = {
			"request": "register",
			"uuid": client_id,
			"username": username,
			"password": password
		}

		# Konvertér til en string
		data = json.dumps(data)
		
		# Omdan til en byte string
		data = data.encode()
		
		# Send data
		sock.sendall(data)
		
		# Modtag data
		data = sock.recv(512)
		Debug.tprint(data)
	# Kører efter "try" eller "except" er executed
	finally:
		if sock:
			print('closing socket')
			sock.close()

'''
Login
'''
def Login():
	global logged_in
	username = input("Enter username: ")
	password = getpass.getpass("Enter password: ")

	try:
		CreateSocket()
		if not sock:
			return None

		# Definér json object
		data = {
			"request": "login",
			"uuid": client_id,
			"username": username,
			"password": password
		}
		# Konvertér til en streng
		data = json.dumps(data)

		# Omdan til en byte string
		data = data.encode()

		# Send data
		sock.sendall(data)

		# Tjekker for svar fra serveren
		data = sock.recv(512)
		Debug.tprint(data)
		data = json.loads(data)
		if data["request"] == "response":
			if data["response"] == "success":
				logged_in = True


	# "finally" kører efter "try" eller "except" er blevet executed
	finally:
		if sock:
			print('closing socket')
			sock.close()

'''
Log ud
'''
def Logout():
	global logged_in
	os.system('cls')
	logged_in = False

	return

'''
GetLatestValue
'''
def GetLatestValue():
	try:
		CreateSocket()
		if not sock:
			return None

		# Definér json object
		data = {
			"request": "latestValue",
			"uuid": client_id,
			"type": "ethusd"
		}

		# Konvertér til en string
		data = json.dumps(data)

		# Omdan til en byte string
		data = data.encode()
		
		# Send data
		sock.sendall(data)
		
		# Modtag data
		data = sock.recv(512)
		Debug.tprint(data)
		data = json.loads(data)
		print('Nuværende værdi: $%.2f' % data["value"])

	# Kører efter "try" eller "except" er executed
	finally:
		if sock:
			print('closing socket')
			sock.close()
	return

'''
GetClosestValueToTimestamp
'''
def GetClosestValueToTimestamp():
	year = int(input("Indtast årstal: "))
	month = int(input("Indtast måned: "))
	day = int(input("Indtast dag: "))
	hour = int(input("Indtast tidspunkt (time): "))
	minutes = int(input("Indtast tidspunkt (minutter): "))
	timestamp = datetime.datetime(year, month, day, hour, minutes).timestamp()
	
	try:
		CreateSocket()
		if not sock:
			return None
			
		# Definér json object
		data = {
			"request": "timestampedValue",
			"uuid": client_id,
			"type": "ethusd",
			"timestamp": timestamp
		}

		# Konvertér til en string
		data = json.dumps(data)

		# Omdan til en byte string
		data = data.encode()
		
		# Send data
		sock.sendall(data)
		
		# Modtag data
		data = sock.recv(512)
		Debug.tprint(data)
		data = json.loads(data)
		print('Daværende værdi: $%.2f' % data["value"])

	# Kører efter "try" eller "except" er executed
	finally:
		if sock:
			print('closing socket')
			sock.close()
	return

'''
Handshake
'''
def Handshake():
	try:
		CreateSocket()

		# Definér json object
		data = {
			"request": "handshake"
		}
		# Konvertér til en streng
		data = json.dumps(data)

		# Omdan til en byte string
		data = data.encode()

		# Send data
		sock.sendall(data)

		# Tjekker for svar fra serveren
		data = sock.recv(512)
		data = json.loads(data)
		if data["request"] == "handshake":
			#print("Modtog ID: " + data["uuid"])
			global client_id
			client_id = data["uuid"]
		#Debug.tprint(data)

	# "finally" kører efter "try" eller "except" er blevet executed
	finally:
		print('closing socket')
		sock.close()