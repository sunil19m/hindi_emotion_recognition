from bs4 import BeautifulSoup
import codecs
import re
import glob
word_synonym={}
path = 'M:/in_progress_download/*.txt'
files = glob.glob(path)
for name in files:
	soup=BeautifulSoup(codecs.open(name,encoding="utf-8"))
	l=len(name)
	x=l-1
	while(x>=0):
		if name[x]=='/'or name[x]=='\\':
			break
		else:
			x=x-1
	word=name[x+1:l-10]
	#print(name,word)
	res=soup.find_all('a',attrs={'class':'in l'})
	ans=[]
	for each in res:
		ans.append(BeautifulSoup(str(each)).getText())
	word_synonym[word]=ans
	#for i in ans:
	#	print(i)