import Options

# Nuværende menuvalg
choice = '0'
while True:  # Sørger for at man bliver sendt tilbage til menuen (loop)
	try:
		if not Options.logged_in:
			# Herunder oprettes en menu, med 4 valgmuligheder
			print("===[ Menu ]===")
			print("1: Registrér")
			print("2: Login")
			print("q: Afslut")
			print("")
			choice = input("Please make a choice: ") # Få input fra brugeren
			
			if choice == "1":
				Options.Register()
			elif choice == "2":
				if Options.client_id == None: # Hvis klienten ikke har fået et ID
					Options.Handshake() # Anmod om nyt ID
				Options.Login()
			elif choice == "q":
				break
			else: # Hvis der vælges en menu som ikke eksisterer
				print("Ukendt valg")
		else:
			# Herunder oprettes en menu, med 3 valgmuligheder
			print("===[ Menu (Logget ind) ]===")
			print("1: Anmod om ETH værdi")
			print("2: Anmod om ETH værdi på et angivet tidspunkt")
			print("3: Log ud")
			print("q: Afslut")
			print("")
			choice = input("Valg: ") # Få input fra brugeren

			# Menu
			if choice == "1":
				break
			elif choice == "2":
				break
			elif choice == "3":
				break
			elif choice == "q":
				break
			else: # Hvis der vælges en menu som ikke eksisterer
				print("Ukendt valg")
	except KeyboardInterrupt:
		print('All done')
		break