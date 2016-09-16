def clearScreen():
	x = 1
	while (x < 50):
		print("\n")
		x += 1

choice = True
while (choice):
	clearScreen()
	try:
		userNum = int(raw_input("Enter starting number (or leave blank for longest number to compute): "))
	except ValueError:
		userNum = 63728127
	currentNum = userNum
	count = 0
	while (currentNum > 1):
		if(currentNum % 2 == 0):
			currentNum = currentNum / 2;
		else:
			currentNum = (currentNum * 3) + 1
		print(currentNum)
		count += 1

	print("Done! Collatz Conjecture took " + str(count) + " steps to get from " + str(userNum) + " to 1.")
	choice = False
	try:
		userKey = int(raw_input("Press Enter to run another number"))
	except ValueError:
		choice = True
