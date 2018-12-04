import json
import socket
import ssl
import getpass
import datetime
import os
import hashlib
from Helpers import Debug

'''
Markerede linje: (225)
Tag datoer og tid fra input og konvertér til timestamp
'''

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
			"password": hashlib.sha256(password.encode()).hexdigest()
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
			"password": hashlib.sha256(password.encode()).hexdigest()
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

			elif data["response"] == "failed":
				print("Login fejlede, brugernavn eller kodeord forkert!")


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

input: 	dd/mm/yyyy hh:mm
		04/12/2018 21:12
'''


def GetClosestValueToTimestamp():
	#date = input("Skriv tidspunktet (dd/mm/yyyy hh:mm): ")
		
	# Splitter strengen indtil 2018
	date = "04/12/2018 21:12"
	print(date)
	
	# Splitter strengen indtil 2018
	newdate = date.split('/')

	# newdate = [ "dd", "mm", "yyyy hh:mm" ]
	day, month = newdate[0], newdate[1]

	# Deler newdate op: [ "yyyy", "hh:mm" ]
	year = newdate[2].split(' ')
	# year = [ "2018", "21:12" ]

	# Tiden deles i "year"-variablen [ "hh", "mm" ]
	hours, minutes = year[1].split(':')
	# hours, minutes = "hh", "mm"

	year = year[0]
	# year = "yyyy"
	

	# Indsæt data i variabler og omdan til tal
	try:
		day = int(day)
		month = int(month)
		year = int(year)
		hours = int(hours)
		minutes = int(minutes)
	except:
		print("Dato ugyldig")
		return
		
	print("Day:    ", day)
	print("Month:  ", month)
	print("Year:   ", year)
	print("Hours:  ", hours)
	print("Minutes:", minutes)

	print("Oneliner: ", day, month, year, hours, minutes)

	timestamp = datetime.datetime(day, month, year, hours, minutes).timestamp()

	
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
		print('Closing socket')
		sock.close()