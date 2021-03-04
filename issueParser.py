import requests
import json
from bs4 import BeautifulSoup
def issueparser(url_repo):
	url = url_repo
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	i=0
	for sol in soup.findAll('div',{'class':'flex-auto'}):
		k = sol.find('a')
		if k != None:

			n = k['href']
			var = n.split('/')
			if var[-1].isdigit():
				print(k.text)
				print(n)
				i = i+1
				url2 = url_repo + var[-1]
				plain_html_text2 = requests.get(url2)
				soup2 = BeautifulSoup(plain_html_text2.text, "html.parser")
				m = soup2.find('td')
				if m != None:
					q = m.find('p')
					if q != None:
						r = q.text
						print(r)

	 	# url2 = "https://www.codechef.com" + l
	 	# plain_html_text2 = requests.get(url2)
	 	# soup2 = BeautifulSoup(plain_html_text2.text, "html.parser")
	 	# m = soup2.find('div',{'class':'ace_content'})
	 	# print(m)i=i+1
	 	# if i==20:
	 	# 	break
	print(i)
	# url = "https://www.codechef.com/viewsolution/34866751"
	# plain_html_text = requests.get(url)
	# soup = BeautifulSoup(plain_html_text.text, "html.parser")
	# for j in soup.findAll('div',{'class':'para-div'}):
	#  	k = j.find('p')
	#  	print(j)
	#  	print(k)
issueparser('https://github.com/EbookFoundation/free-programming-books/issues')