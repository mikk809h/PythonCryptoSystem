'''
Login giver success
Registrér det på db
Få adgang til data fra db
lav en "logged in" menu
'''
import socket
import json
import hashlib
import uuid
from Helpers import Database
from Helpers import Response
from Helpers import Debug

# Handshake list
handshakes = {}

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 88)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print('waiting for a connection')
	connection, client_address = sock.accept()

	try:
		print('connection from', client_address)

		# Receive the data in small chunks and retransmit it
		while True:
			data = connection.recv(512)

			if data:
				Debug.tprint(data)

				# Login / Register
				data = json.loads(data)

				if data["request"] == "handshake":
					print("handshake")

					response_data = {
						"request": "handshake",
						"uuid": str(uuid.uuid4())
					}

					handshakes[response_data["uuid"]] = False
					
					Response.reply(connection, response_data)

					# Debug print the list of handshakes
					Debug.tprint(handshakes)

				elif data["request"] == "login":
					print("Login")
					response_data = {
						"request": "response",
						"response": "failed"
					}

					# Validér ID
					if data["uuid"]:
						if not handshakes[data["uuid"]]:
							query = 'SELECT * FROM users WHERE username="' + data["username"] + '" AND password="' + hashlib.sha256(data["password"].encode()).hexdigest() + '"'
							print(query)

							# How many users match these credentials
							users = Database.query("crypto", query, None)
							if len(users) == 1:
								print("Logged in")
								handshakes[data["uuid"]] = True  # Sæt uuid til True (Logget ind)
								response_data["response"] = "success"
					else:
						# ID ikke specificeret (Mangler at lave et handshake)
						print("Unspecified ID")

					Response.reply(connection, response_data)

				elif data["request"] == "register":
					print("Register")
					response_data = {
						"request": "response",
						"response": "success"
					}

					# Registrér bruger
					query = 'INSERT INTO users(username, password) VALUES ("' + data["username"] + '", "' + hashlib.sha256(data["password"].encode()).hexdigest() + '")'
					print(query)

					Database.query("crypto", query, None)
					Response.reply(connection, response_data)
					
				elif data["request"] == "latestValue":
					print("Fetching latest value")
					response_data = {
						"request": "response",
						"response": "success",
						"value": None,
					}
					selectedCurrencyPair = "btcusd"
					if data["type"] == "ethusd":
						selectedCurrencyPair = "ethusd"
					
					# Get latest value
					query = 'SELECT value FROM %s ORDER BY timestamp DESC LIMIT 1' % selectedCurrencyPair
					print(query) # Debug

					response_data["value"] = Database.query("crypto", query, None)[0][0]

					print(response_data["value"])
					Response.reply(connection, response_data)

				elif data["request"] == "timestampedValue":
					
					print("Fetching values closest to your specified timestamp")
					response_data = {
						"request": "response",
						"response": "success",
						"value": None,
					}
					selectedCurrencyPair = "btcusd"
					if data["type"] == "ethusd":
						selectedCurrencyPair = "ethusd"
					
					# Timestamp
					query = 'SELECT value FROM %s ORDER BY ABS(timestamp - %s) LIMIT 1' % (selectedCurrencyPair, data["timestamp"])
					print(query) # Debug

					response_data["value"] = Database.query("crypto", query, None)[0][0]
					
					print(response_data["value"])
					Response.reply(connection, response_data)

				else:
					print("Unknown request: " + data["request"])

				# print('sending data back to the client')
				# connection.sendall(b"Confirmed")
			else:
				print('no more data from', client_address)
				break
	except:
		print("Error")
	finally:
		# Clean up the connection
		connection.close()
