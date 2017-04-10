from bs4 import BeautifulSoup

import requests

#url = raw_input("Enter a website to extract the URL's from: ")

for year in range(2000, 2006, 1):
	print("year: "+str(year))
	url = "smriti.com/hindi-songs/year-"+str(year)
	r  = requests.get("http://" +url)
	data = r.text

	#soup = BeautifulSoup(data, "lxml")
	soup = BeautifulSoup(data, "html.parser")
	filename = "output"+str(year)+".txt"
	output_file = open(filename, "w")
	for link in soup.find_all('a'):
		if "utf8" in link.get('href'):
			output_file.write("http://smriti.com"+link.get('href')+"\n")
	output_file.close()