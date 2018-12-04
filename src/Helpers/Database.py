import mysql.connector
from mysql.connector import Error

hostDataMikkel = {
	"host": 'localhost',
	"user": 'Crypto',
	"password": 'MULT133akut',
}

hostDataMartin = {
	"host": 'localhost',
	"user": 'root',
	"password": '',
}


def query(database, query, args):
	''' Connect to MySQL database '''
	conn = None
	try:
		conn = mysql.connector.connect(host=hostDataMikkel["host"],
									   database=database,
									   user=hostDataMikkel["user"],
									   password=hostDataMikkel["password"])
		if conn.is_connected():
			print('Forbundet til MySQL database')

			cursor = conn.cursor()
			cursor.execute(query, args)

			if cursor.lastrowid:
				print('last insert id', cursor.lastrowid)
				return True
			else:
				user = cursor.fetchall()
				return user

	except Error as e:
		print(e)

	finally:
		conn.commit()
		conn.close()
