#!/usr/bin/env python
# Copyright 2017 Dave Machado

import json
import os
import platform
import urllib2

alphaSet = ['A', 'B', 'C', 'D']
results = []
NUM_ROUNDS = -1

def clearScreen():
	if (platform.system() == "Windows"):
		os.system('cls')
	else:
		os.system('clear')

def pressKeyToContinue():
	raw_input("\nPress Enter to continue...")

def callMenu():
	print("****************************************************************")
	print("*                          Trivia Game                         *")
	print("*                     built by Dave Machado                    *")
	print("*                                                              *")
	print("*       This program is protected by the Apache License        *")
	print("****************************************************************")

def printJSON(data):
	str = json.dumps(data)
	print(str)

def getQuestions():

	url = 'https://api.symerit.com/?count='\
		+ NUM_ROUNDS + '&key=8675309'
	req = urllib2.Request(url)
	req.add_header('x-api-key','123456')
	response = urllib2.urlopen(req).read()
	jsonvalues = json.loads(response)
	return jsonvalues

def playGame():
	count = 1
	score = 0
	data = getQuestions()
	for each in data['results']:
		clearScreen()
		ques = each['question']
		correctAns = each['answer']

		print("----- QUESTION " + str(count) + " / " + NUM_ROUNDS + " -----")
		print("-----   Score: " + str(score) + "   -----\n")
		print(str(ques) + "\n")
		for x in alphaSet:
			print(x + ") " + each[x])

		choice = (raw_input("\nAnswer: ")).upper()
		while choice not in alphaSet:
			choice = raw_input(("Invalid choice, try again: ")).upper()

		if choice == correctAns:
			print("Correct!")
			results.append({"number":count, "result":"Correct"})
			score += 1
		else:
			print("Wrong! The answer was " + correctAns)
			results.append({"number":count, "result":"Incorrect"})
		count += 1
		pressKeyToContinue()
	clearScreen()
	print("------ GAME OVER ------")
	res = score / float(NUM_ROUNDS)
	print("Final Score: " + str(score) + " or " + str(round(res, 2)) + "%")
	print("\nROUND\tRESULT")
	for each in results:
		print(str(each['number']) + "\t" + each['result'])
	ret = raw_input("Play again? (y)es or (n)o : ")
	if ret.upper() == 'Y':
		return True
	else:
		return False

def main():
	global NUM_ROUNDS
	clearScreen()
	callMenu()
	while True:
		NUM_ROUNDS = raw_input("\nNumber of Rounds: ")
		if (playGame() == False):
			break

if __name__ == '__main__':
    main()
