import json

def reply(connection, data):
	# Konvertér til en streng
	response_data = json.dumps(data)
	# Omdan til en byte string
	response_data = response_data.encode()

	# Reply with uuid
	connection.sendall(response_data)
