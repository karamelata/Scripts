#!/usr/bin/env python
# Copyright 2017 Dave Machado

import json
import os
import platform
import urllib

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
	url = 'https://s4ycy5dmu8.execute-api.us-east-1.amazonaws.com/api?num='\
		+ NUM_ROUNDS
	response = urllib.urlopen(url).read()
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

		print("----- QUESTION " + str(count) + "/" + NUM_ROUNDS + " -----")
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
	print("Final Score: " + str(score))
	print("\nROUND\tRESULT")
	for each in results:
		print(str(each['number']) + "\t" + each['result'])

def main():
	global NUM_ROUNDS
	clearScreen()
	callMenu()
	NUM_ROUNDS = raw_input("\nNumber of Rounds: ")
	playGame()

if __name__ == '__main__':
    main()
