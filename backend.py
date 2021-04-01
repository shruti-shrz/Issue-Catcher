import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
from issueParser import *
from flask_cors import CORS
from settings import MONGOPASS
import threading
from datetime import *

cluster =  MongoClient('mongodb+srv://pinky:'+MONGOPASS+'@cluster0.hfcw3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['IssueDB']
collection = db['issues']
k = "hello"
ans = []
app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST', 'GET'])
def bootstrap():
	global ans
	global k
	if request.method == 'POST':
		if not request.form:
			print("nothing!!!")
			return jsonify({'error' : 'Empty request'})
		else:
			var = request.form
			k = var['issue']
			print(k,type(k))
			myquery = {"url":k}
			myissue = None
			myissue = collection.find_one(myquery)
			#print(ans)
			# if myissue == None:
			#ans = get_ans(k)
			# 	i = {'url' : k, 'ans': ans}
			# 	collection.insert_one(i)
			# else:
			# 	ans = myissue['ans']
			# if len(ans) > 0:
			# 	return jsonify(ans)
			# else:
			# 	return jsonify({'error':'Similar Issues Not Found'})
			if myissue == None:
				ans = get_ans(k)
				i = {}
				i['url'] = k
				i['ans'] = ans
				i['timestamp'] = date.today()
				collection.insert_one(i)
			else:
				print("Picked from db!")
				ans = myissue['ans']
				print(ans)
			def fill_other_issues(**kwargs):
				url_rep = kwargs.get('post_data', {})
				other_issue.clear()
				get_other_issues(url_rep)
				for i in other_issue:
					myquery = {"url":i}
					myissue = None
					myissue = collection.find_one(myquery)
					if myissue == None:
						ans = get_ans(i)
						j = {}
						j['url'] = i
						j['ans'] = ans
						collection.insert_one(j)
					else:
						print("issue already there!!")
			thread = threading.Thread(target=fill_other_issues, kwargs={'post_data': k})
			thread.start()
			if len(ans) > 0:
			 	return jsonify({'url' : ans})
			else:
			 	return jsonify({'error':'Similar Issues Not Found'})
	return jsonify({'url' : ans})


@app.route('/admin', methods=['GET'])
def admin():
	today = date.today()
	i = 0
	limit = 20
	flag = 0
	c = 0
	while flag == 0:
		issues = collection.find({}, {'timestamp': {'$lt': today - timedelta(days = 30)}}).skip(i*limit).limit(limit)
		if issues == None:
			flag = 1
			break
		for issue in issues:
			if issue != None:
				new_res = {'$set': {'ans': get_ans(issue['url'])}}
				collection.update_one({'url': issue['url']}, new_res)
				c += 1
			else:
				flag = 1
				break
		i += 1
	return jsonify({'res': str(c) + " issues updated"})				


if __name__ == "__main__":
    app.run(debug=True)