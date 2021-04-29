import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
from issueParser import *
from flask_cors import CORS
from settings import MONGOPASS
import threading
from datetime import *

# getting db collection to query on and insert to
cluster =  MongoClient('mongodb+srv://pinky:'+MONGOPASS+'@cluster0.hfcw3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['IssueDB']
collection = db['issues']

k = ""
ans = []
app = Flask(__name__)
CORS(app)

# main route
@app.route('/', methods=['POST', 'GET'])
def bootstrap():
	global ans
	global k
	if request.method == 'POST':
		if not request.form:
			print("nothing!!!")  # empty request: error
			return jsonify({'error' : 'Empty request'})
		else:
			var = request.form
			k = var['issue']
			print(k,type(k))
			myquery = {"url":k}
			myissue = None
			myissue = collection.find_one(myquery)  # seeing if input issue already exists in DB
			if myissue == None:    # not found in DB
				ans = get_ans(k)    # THE function which gives similar issues 
				i = {}
				i['url'] = k
				i['ans'] = ans
				i['timestamp'] = datetime.today()
				if len(ans) > 0:
					collection.insert_one(i)   # inserting into DB
			else:
				print("Picked from db!")    # found in DB
				ans = myissue['ans']
				#print(ans)
			def fill_other_issues(**kwargs):    # function to do the entire process for other issues in the backgorund
				#global other_issues
				url_rep = kwargs.get('post_data', {})
				other_issues.clear()
				v = url_rep.rfind('/')
				url_rep = url_rep[:v]
				get_other_issues(url_rep)
				#print(other_issues, "     ==    ")
				for i in other_issues:
					i = "https://github.com" + i
					myquery = {"url":i}
					myissue = None
					myissue = collection.find_one(myquery)
					if myissue == None:
						ans = get_ans(i)
						j = {}
						j['url'] = i
						j['ans'] = ans
						#print(j)
						#print("------NEXT------")
						collection.insert_one(j)
					else:
						print("issue already there!!")
			
			# THE FOLLOWING 2 LINES TO UNCOMMENT TO ENABLE THE ABOVE FEATURE OF BACKGROUND COMPUTATION OF OTHER ISSUES
			# thread = threading.Thread(target=fill_other_issues, kwargs={'post_data': k})
			# thread.start()

			if len(ans) > 0:
			 	return jsonify({'url' : ans})   # returning similar issues
			else:
			 	return jsonify({'message':'Similar Issues Not Found. Sorry!!'})
	return jsonify({'url' : ans})

# admin route , to update DB if entries are more than 15 days old
@app.route('/admin', methods=['GET', 'POST'])
def admin():
	today = datetime.today()
	i = 0
	limit = 20
	flag = 0
	c = 0
	while flag == 0:
		issues = collection.find({}, {'timestamp': {'$lte': ['$timestamp', today - timedelta(days = 15)]}, 'url': 1}).skip(i*limit).limit(limit)
		c = 0
		for issue in issues:
			print(issue)
			if issue != None:
				new_res = {'$set': {'ans': get_ans(issue['url']), 'timestamp': today}}
				collection.update_one({'url': issue['url']}, new_res)
				c += 1
		if c < limit:
			break
		i += 1
	return jsonify({'res': str(i* limit + c) + " issues updated"})				


if __name__ == "__main__":
    app.run(debug=True)
