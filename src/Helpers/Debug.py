import json

def tprint(data):
	try:
		print(json.dumps(json.loads(data), indent=4))
	except:
		if type(data) == "string":
			print(data)
		else:
			try:
				print(data.decode())
			except:
				print(data)
