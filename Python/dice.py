#!/usr/bin/env python

# Copyright 2017 Dave Machado
# Description: Randomly roll X number of Y-sided dice

from random import randint
from sys import argv

def rollDice(numOfDice, numOfSides):
	for each in xrange(numOfDice):
		print(randint(1, numOfSides))

if len(argv) > 1:
	numDice = int(argv[1])
	if len(argv) > 2:
		rollDice(numDice, int(argv[2]))
	else:
		rollDice(numDice, 6)
else:
	print("Invalid arguments- try: " + argv[0] +" [number of dice] [number of sides]")
