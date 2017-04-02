import json
import os
import platform
import urllib2

NUM_ROUNDS = -1
ALPHA_SET = ['A', 'B', 'C', 'D']

def clearScreen():
	if (platform.system() == "Windows"):
		os.system("cls")
	else:
		os.system("clear")

def pressKeyToContinue():
	raw_input("\nPress Enter to Continue...")

def printJSON(data):
	str = json.dumps(data)
	print(str)

def getQuestions():
	url = ""
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	json_raw = json.loads(response.read())
	return json_raw

def playGame():
	round_count = 1
	score = 0
	data = getQuestions()
	for each in data['results']:
		clearScreen()
		ques = each['question']
		correctAns = each['answer']
		print("----- QUESTION " + str(round_count) \
			+ " / " + str(NUM_ROUNDS) + "-----")
		print("----- SCORE: " + str(score) + " -----\n")
		print(ques + "\n")
		for choice in ALPHA_SET:
			print(choice + ") " + each[choice])

		user_ans = (raw_input("\nAnswer: ")).upper()
		while user_ans not in ALPHA_SET:
			user_ans = (raw_input("Invalid choice! Try again: ")).upper()

		if user_ans == correctAns:
			print("Correct!")
			score += 1
		else:
			print("Wrong! The answer was " + correctAns)
		round_count += 1
		pressKeyToContinue()

def main():
	global NUM_ROUNDS
	clearScreen()
	while True:
		NUM_ROUNDS = raw_input("Please enter number of rounds: ")
		if (playGame() == False):
			break

if __name__ == '__main__':
	main()














