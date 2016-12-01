#!/usr/bin/env python

import getch
import os

page = 0

name = input("Enter name of pdf: ")

while(1):
	print("Press q for exit, Space for scanning, and d for done")
	x = getch.getch()
	if(x == 'q'):
		exit()
	elif(x == ' '):
		print("Starting scan of page " + str(page+1))
		os.system("scanimage --device genesys:libusb:001:004 --format=tiff > scan" + str(page) + ".tiff")
		page += 1
		print("Scan done")
	elif(x == 'd'):
		print("Collecting tiff pages")
		os.system("tiffcp scan*.tiff magazine.tiff");
		print("Making pdf file")
		os.system("convert magazine.tiff '" + name + ".pdf'")
		print("Removing tiffs")
		os.system("rm *.tiff")
		print("Done resetting vars")
		page = 0
		name = input("Enter name of pdf: ")


