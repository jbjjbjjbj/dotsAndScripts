#!/usr/bin/env python

from bs4 import BeautifulSoup

import requests
import os

res = requests.get('https://phra.gs/futurama/comics/')

soup = BeautifulSoup(res.text, "html.parser")

elems = soup.select('table')[0].find_all("td")

#links = []

for e in elems[2:]:
	if(len(e.find_all("a")) > 0):
		#print(e.find("a").attrs["href"])
		#links.append(e.find("a").attrs["href"])
		os.system("wget 'https://phra.gs/futurama/comics/" + e.find("a").attrs["href"] + "'")





