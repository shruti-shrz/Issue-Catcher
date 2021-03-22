import requests
import json
from bs4 import BeautifulSoup
count = 975
s_c=0
list_words = set()
f=open('technical_keyword.txt','a')
# lines_seen = set()  # holds lines already seen
# outfile = open('tech.txt', "w")
# infile = open('technical_keyword.txt', "r")
# print("The file bar.txt is as follows")
# for line in infile:
#     #print line
#     if line not in lines_seen:  # not a duplicate
#         outfile.write(line)
#         lines_seen.add(line)
# outfile.close()
# print("end")


def getwords(url):
	global count
	global s_c
	global list_words
	global f
	c = "s"
	count +=1
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	ques = soup.find('div',{'id':'tags_list'})
	tags = ques.findAll('div',{'class':'grid'})
	for sel in tags:
		s = sel.find('div',{'class':'grid--cell'})
		tg = s.find('a')
		#print("cjhe2")
		if tg!=None:
			if c=="s":
				c = tg.text
				print(tg.text)
				f.write(tg.text+'\n')
			elif c!=tg.text:
				f.write(tg.text+'\n')
				print(tg.text)
				c = tg.text
				s_c+=1
			


			#print(tg.text)
			#list_words.add(tg.text)
			
		
	#next_page = soup.find('div',{'class':'s-pagination pager fr'})
	if count == 1793:
		return
	#nx = next_page.findAll('a',{'class':'s-pagination--item'})
	url_next = "https://stackoverflow.com/tags?page="+str(count)+"&tab=popular"
	getwords(url_next)
getwords('https://stackoverflow.com/tags?page=975&tab=popular')
#l1 = list(list_words)

# for ele in l1:
#     f.write(ele+'\n')

f.close()
print(s_c)
print(count)