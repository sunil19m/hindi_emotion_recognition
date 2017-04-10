import codecs
import json
import urllib2
from bs4 import BeautifulSoup

url_files = ["output2000.txt", "output2001.txt", "output2002.txt", "output2003.txt", "output2004.txt", "output2005.txt"]

for file in url_files:

	output_file = file.split(".")
	output_file = output_file[0] + ".json"
	print (output_file)
	fp = open(output_file,"w")
	songs = {}
	id = 0

	with open(file,"r") as f:
		for url in f:
			id = id + 1
			songs[id] = {}
			response = urllib2.urlopen(url)
			html = response.read()

			soup = BeautifulSoup(html, "html.parser")

			for e in soup.findAll("br"):		# Remove all <br> tags 
				e.extract()

			songName = soup.findAll("h1")

			if (len(songName) > 1):
				songName = songName[1].contents[0]
			else:
				songName = ""

			songs[id]["SongName"] = songName


			songDetails = soup.find("ul", {"class" : "pstats"}).findAll("li")

			for details in songDetails:
				links = details.findAll("a")
				name = details.find("b").contents[0]

				if (name.startswith("Mov")):
					songs[id]["MovieName"] = ""
					for link in links:
						songs[id]["MovieName"] = link.contents[0]

				elif (name.startswith("Sin")):
					songs[id]["Singers"] = []
					for link in links:
						songs[id]["Singers"].append(link.contents[0])

				elif (name.startswith("Mus")):
					songs[id]["MusicDirector"] = []
					for link in links:
						songs[id]["MusicDirector"].append(link.contents[0])

				elif (name.startswith("Mus")):
					songs[id]["MusicDirector"] = []
					for link in links:
						songs[id]["MusicDirector"].append(link.contents[0])

				elif (name.startswith("Lyr")):
					songs[id]["Lyricist"] = []
					for link in links:
						songs[id]["Lyricist"].append(link.contents[0])

				elif (name.startswith("Act")):
					songs[id]["Actors"] = []
					for link in links:
						songs[id]["Actors"].append(link.contents[0])


			songLyrics = soup.find("div", {"class" : "songbody"}).findAll("p")

			temp_list = []
			for line in songLyrics:										# Each <p> tag in the div	
				for contents in line:									# Each <br> tag in <p> tag
					temp_list.append(contents.encode("utf8") + " ")		# Append lyrics to a temp list	

			temp_str = ''.join(temp_list)								# Convert the list to a string
			songs[id]["lyrics"] = temp_str								# Store in the songs dictionary
							
	json.dump(songs, fp)
