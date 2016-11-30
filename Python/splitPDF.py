#!/usr/bin/python3

# Copyright 2016 Dave Machado

# Split one PDF into individual pages
# $ python3 splitPDF.py [original.pdf] [number of pages]

import os
import sys

if len(sys.argv) != 2:
	print(sys.argv[0] + " [original.pdf] [number of pages]")
	sys.exit()

input_pdf = sys.argv[1]
number_of_pages = int(sys.argv[2])

for i in range(1, number_of_pages +1):
    os.system("gs -q -dBATCH -dNOPAUSE -sOutputFile=page{page:02d}.pdf"
              " -dFirstPage={page} -dLastPage={page}"
              " -sDEVICE=pdfwrite {input_pdf}"
              .format(page=i, input_pdf=input_pdf))

