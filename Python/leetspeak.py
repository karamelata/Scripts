#!/usr/bin/env python3

from sys import argv, exit

encode = {
    'a': '4',
    'b': '|3',
    'c': '{',
    'd': '[)',
    'e': '3',
    'f': '|=',
    'g': '6',
    'h': '/-/',
    'i': '!',
    'j': '_|',
    'k': '|<',
    'l': '1_',
    'm': '(\/)',
    'n': '(\)',
    'o': '()',
    'p': '[]D',
    'q': '(,)',
    'r': '[Z',
    's': '$',
    't': '-|-',
    'u': '|_|',
    'v': '\/',
    'w': '(/\)',
    'x': '}{',
    'y': '\'/',
    'z': "\"/_"
}
decode = dict((v,k) for k,v in encode.items())

if len(argv) < 1:
	print("need to indicate encode or decode")
	exit(1)

if argv[1] == 'encode' or argv[1] == 'e':
	str = input("Enter a string to encode: ")
	new_str = ""
	for c in str.lower():
		if c in encode:
			new_str += encode[c]
		else:
			new_str += c
	print(new_str)
elif argv[1] == "decode" or argv[1] == 'd':
	str = input("Enter a string to decode: ")
	tok = ""
	new_str = ""
	for c in str:
		tok += c
		if tok in decode:
			new_str += decode[tok]
			tok = ""
		if c == ' ':
			new_str += ' '
			tok = ""
	print(new_str)

