import requests
import json
from bs4 import BeautifulSoup
from key_extract import *
from similarBert import *
from code_preprocessor import *
import re

issues_1000 = []
issues_1001 = []
issue = {}
issue_score = []
nex_count = 1
other_issues = []
code_ans = []

# function to scrape other issues in current repo, to aid the commented code background processing
def get_other_issues(repo_url):
	global nex_count
	global other_issues
	if nex_count ==1:
		url= repo_url + "?page="+str(nex_count)+"&q=is%3Aissue+is%3Aopen"
	else:
		url = repo_url
	nex_count +=1
	
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	res = soup.find('div', {'aria-label':'Issues'})
	res2 = res.findAll('div', {'class':'flex-auto min-width-0 p-2 pr-3 pr-md-2'})
	for sol in res2:
		h = sol.find('a')
		other_issues.append(h['href'])
	res = soup.find('div',{'role':'navigation'})
	if res != None:
		res2 = res.find('a',{'rel':'next'})
	if res2==None or res == None:
		return
	url_next = 'https://github.com' + res2['href']
	get_other_issues(url_next)

# function which gives the top 5 similar issues and their URLs and scores
def get_ans(input_issue):
	global issue
	global code_ans
	url = input_issue
	ans = []
	plain_html_text = requests.get(url)
	issue['url'] = url
	
	# scraping necessary details of the input issue
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	title = soup.find('span', {'class':'js-issue-title markdown-title'})
	title = title.text.strip()
	issue['title'] = re.sub(r'\[.+\]','',title)
	issue['body'] = ''
	body = soup.find('div', {'class':'edit-comment-hide'})
	for b in body.findAll('td', {'class':'comment-body'}):
		issue['body'] += b.text.replace('\n',' ').strip()
	# issue['labels'] = []
	# labels = soup.findAll('a', {'class': 'IssueLabel'})
	# for label in labels:
	# 	issue['labels'].append(label.text.strip())
	
	code = body.find('code')
	if code != None:
		issue['code'] = code.text
	else:
		issue['code'] = ''

	repo_url_end = url.find('/issues') 
	repo_url = url[0:repo_url_end]
	repo_html_text = requests.get(repo_url)
	soup = BeautifulSoup(repo_html_text.text, "html.parser")
	# issue['lang'] = []
	# for lang in soup.findAll('span',{'class':'color-text-primary text-bold mr-1'}):
	# 	l = lang.text.strip()
	# 	issue['lang'].append(l)
	# print("INPUT ISSUE:")
	# print(issue)

	# thread to get issues based on code in input issue starts here
	
	input_key = nlp_LDA(issue['title'])   # getting keywords from title of input issue
	# getting scraped issues that we get from query
	if len(input_key) >= 4:
		get_1000_issues(input_key[0:4], url)  
	else:
		get_1000_issues(input_key[0:len(input_key)], url)

	#input_issue_key = nlp_LDA(issue['title']+issue['body']) # getting key words
	# preparing document list for BERT similarity model
	text_list = []
	url_list = []
	text_list.append(issue['title'] + issue['body'])
	url_list.append(url)
	for i in issues_1000:
		text_list.append(i['title'] + i['body'])
		url_list.append(i['url'])
	ans = getSimilarBert(url_list, text_list)  # getting similarity scores for input documents
	for i in range(1, min(6, len(ans))):
		ans[i]['score'] = int(ans[i]['score']*100)

	# wait for thread to finish
		
	if issue['code'] != '':
		search_code_issues(issue)
		new_ans = ans[1:4] + code_ans[1:3]
		#new_ans = sorted(new_ans, key = lambda i: i['score'],reverse=True)
		# print('NEWANS:')
		# print(new_ans)
		return new_ans
	else:   # in case of no code in input issue
		# print('ANS:')
		# print(ans[1:6])
		return ans[1:6]

# function that runs on the thread created for code related search
def search_code_issues(issue):
	global code_ans
	# print('HI IN CODE')
	
	# preprocessing of code to get relevant words 
	code_words = code_preprocess(issue['code'])
	keys = '+'.join(code_words[0: min(len(code_words), 4)])
	url = 'https://github.com/search?q=' + keys + '&type=issues'
	get_issues(url, issue['url'], False)
	text_list = []
	url_list = []
	text_list.append(issue['title'] + issue['body'])
	url_list.append(issue['url'])	
	for i in issues_1001:
		text_list.append(i['title'] + i['body'])
		url_list.append(i['url'])
	code_ans = getSimilarBert(url_list, text_list)   # getting similarity scores
	for i in range(1, min(6, len(code_ans))):
		code_ans[i]['score'] = int(code_ans[i]['score']*100)
	# print('HI CODE DONE')

# querying for issues using keywords extracted
def get_1000_issues(keywords, inp_url):
	keys = '+'.join(keywords)
	url = 'https://github.com/search?q=' + keys + '+in%3Atitle&type=issues'
	get_issues(url, inp_url)

count = 0
# getting info for each issue from the pages obtained after querying
def get_issues(url, inp_url, flag = True):
	global count
	count += 1
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	issues_10 = soup.findAll('div',{'class':'issue-list-item'})
	for sel in issues_10:
		sel = sel.find('div',{'class': 'markdown-title'}).find('a')
		if 'issues' in sel['href']:
			sel_issue_url = "https://github.com" + sel['href']
			if sel_issue_url != inp_url:
				issue_parser(sel_issue_url, flag)
		elif 'pull' in sel['href']:
			sel_pull_url = "https://github.com" + sel['href']
			pull_req_parser(sel_pull_url, flag)
	next_page = soup.find('a',{'class':'next_page'})
	if next_page == None or count == 2:
		return
	url_next = "https://github.com" + str(next_page['href'])
	get_issues(url_next, inp_url, flag)

# scraping info for each issue
def issue_parser(url, flag = True):
	if url == None:
		return
	issue = {}
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	title = soup.find('span', {'class':'js-issue-title markdown-title'})
	issue['title'] = ''
	if title != None:
		issue['title'] = title.text.strip()
	issue['body'] = ''
	body = soup.find('div', {'class':'edit-comment-hide'})
	if body != None:
		for b in body.findAll('td', {'class':'comment-body'}):
			issue['body'] += b.text.replace('\n',' ').strip()
	# issue['labels'] = []
	# labels = soup.findAll('a', {'class': 'IssueLabel'})
	# if labels != None:
	# 	for label in labels:
	# 		issue['labels'].append(label.text.strip())
	issue['url'] = url
	# print("ISSUE PARSER")
	# print(issue)
	if flag == True:
		issues_1000.append(issue)
	else:
		issues_1001.append(issue)

# scraping info for each pull request
def pull_req_parser(url, flag = True):
	if url == None:
		return
	issue = {}
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
	title = soup.find('span', {'class':'js-issue-title markdown-title'})
	issue['title'] = ''
	if title != None:
		issue['title'] = title.text.strip()
	issue['body'] = ''
	body = soup.find('div', {'class':'edit-comment-hide'})
	if body != None:
		for b in body.findAll('td', {'class':'comment-body'}):
			issue['body'] += b.text.replace('\n',' ').strip()
	issue['url'] = url
	# print("\nPULL REQUEST PARSER")
	# print(issue)
	if flag:
		issues_1000.append(issue)
	else:
		issues_1001.append(issue)

# scraping details of repo : NOT USING ANYMORE
def repo_parser(url_repo):
	url = url_repo
	plain_html_text = requests.get(url)
	soup = BeautifulSoup(plain_html_text.text, "html.parser")
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
		
	#print(repo_details)
	return repo_details

	