import requests
import json
from bs4 import BeautifulSoup

issues_1000 = []

def get_ans(input_issue):
	ans = {}
	issue = {}
	url = input_issue
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	title = soup.find('span', {'class':'js-issue-title markdown-title'})
	issue['title'] = title.text.strip()
	issue['body'] = ''
	body = soup.find('div', {'class':'edit-comment-hide'})
	for b in body.findAll('td', {'class':'comment-body'}):
		issue['body'] += b.text.replace('\n',' ').strip()
	issue['labels'] = []
	labels = soup.findAll('a', {'class': 'IssueLabel'})
	for label in labels:
		issue['labels'].append(label.text.strip())
	repo_url_end = url.find('/issues') 
	repo_url = url[0:repo_url_end]
	repo_html_text = requests.get(repo_url)
	soup = BeautifulSoup(repo_html_text.text, "html.parser")
	issue['lang'] = []
	for lang in soup.findAll('span',{'class':'color-text-primary text-bold mr-1'}):
		l = lang.text.strip()
		issue['lang'].append(l)
	print(issue)
	return ans


def repo_parser(url_repo):
	url = url_repo
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	i=0
	repo_details = {}
	#tags = soup.findAll('div',{'class':'f6'})
	#print(tags)
	repo_details['tag'] = []
	for tag in soup.findAll('a',{'class':'topic-tag topic-tag-link'}):
		t = tag.text.strip()
		repo_details['tag'].append(t)

	repo_details['lang'] = []
	for lang in soup.findAll('span',{'class':'color-text-primary text-bold mr-1'}):
		l = lang.text.strip()
		repo_details['lang'].append(l)
		

	for forks in soup.findAll('a',{'class':'social-count'}):
		f = forks.text.strip().replace(',', '')
		if f[-1] == 'k':
			f = float(f[0:len(f)-1])*1000
		else:
			f = float(f)
		if "stars" not in repo_details.keys():
			repo_details['stars'] = f
		else:
			repo_details['forks'] = f
		

	url_issues = url + '/issues'
	plain_html_text_i = requests.get(url_issues)
	soup_i = BeautifulSoup(plain_html_text_i.text, "html.parser")
	# for open_issue in soup_i.findAll('a',{'class':'btn-link selected'}):
	# 	print(open_issue.text)
	for issue in soup_i.findAll('a',{'class':'btn-link'}):
		
		iss = issue.text.strip()
		var = iss.split(' ')
		f = var[0].replace(',', '')
		if f[-1] == 'k':
			f = float(f[0:len(f)-1])*1000
		else:
			f = float(f)
		if "open_issue" not in repo_details.keys():
			if var[1]=="Open":
				repo_details['open_issue'] = f
		if "close_issue" not in repo_details.keys():
			if var[1]=="Closed":
				repo_details['close_issue'] = f
		
	print(repo_details)
	return repo_details
	# for sol in soup.findAll('div',{'class':'flex-auto'}):
	# 	k = sol.find('a')
	# 	if k != None:
	# 		n = k['href']
	# 		var = n.split('/')
	# 		if var[-1].isdigit():
	# 			print("Issue:  "+k.text)
	# 			print(n)
	# 			i = i+1
	# 			url2 = url_repo + '/' +var[-1]
	# 			plain_html_text2 = requests.get(url2)
	# 			soup2 = BeautifulSoup(plain_html_text2.text, "html.parser")
	# 			m = soup2.find('td')
				
	# 			if m != None:
	# 				q = m.find('p')
	# 				if q != None:
	# 					r = q.text
	# 					print("Issue Description:  "+r)
						

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
count = 0
def getrepos(url):
	global count
	count += 1
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	tag = soup.findAll('li',{'class':'repo-list-item'})
	for sel in tag:
		sel = sel.find('a')
		print(sel['href'])
		repo_url = "https://github.com" + sel['href']
		repo_parser(repo_url)
	next_page = soup.findAll('a',{'class':'next_page'})
	if next_page == None or count == 2:
		return
	url_next = "https://github.com" + str(next_page[0]['href'])
	getrepos(url_next)


#repo_parser('https://github.com/tensorflow/tensorflow')
#getrepos('https://github.com/search?p=1&q=is%3Apublic&type=Repositories')

get_ans('https://github.com/tensorflow/tensorflow/issues/47973')