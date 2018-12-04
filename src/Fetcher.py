# API : https://www.bitstamp.net/api/v2/ticker/ethusd/

import urllib.request
import json
import time
from Helpers import Debug
from Helpers import Database

'''
	Supported values for currency_pair: 
	btcusd, btceur, eurusd, 
	xrpusd, xrpeur, xrpbtc,
	ltcusd, ltceur, ltcbtc,
	ethusd, etheur, ethbtc,
	bchusd, bcheur, bchbtc
'''

# Variabler
currency_pair = "ehtusd"
url = "https://www.bitstamp.net/api/v2/ticker/ethusd/"
page = ""
req = urllib.request.Request(url) # Sætter "req" til resultatet af urllib.request.Request(url)

def insert(data):
	query = "INSERT INTO ethusd(value,high,low,vwap,volume,bid,ask,timestamp,open) " \
			"VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (data["last"], data["high"], data["low"], data["vwap"], data["volume"], data["bid"], data["ask"], data["timestamp"], data["open"])

	Database.query("crypto", query, args)

starttime=time.time()
while True:
	Debug.tprint("Sender forespørgsel")
	with urllib.request.urlopen(req) as response: # Åbner resultatet af "req"
		page = response.read() # Scriptet læser den modtagne data og lagrer det i "page"

	data = json.loads(page.decode('UTF-8'))
	Debug.tprint(data)

	insert(data)
	Debug.tprint("Venter...")
	time.sleep(60.0 - ((time.time() - starttime) % 60.0)) # Her sættes en timer på 30 sek. igang og så sender den endnu en request
