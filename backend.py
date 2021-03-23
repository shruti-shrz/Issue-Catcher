import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
from issueParser import *
from flask_cors import CORS
from settings import MONGOPASS
cluster =  MongoClient('mongodb+srv://pinky:'+MONGOPASS+'@cluster0.hfcw3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['IssueDB']
collection = db['issues']
k = "hello"
ans = []
app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST' , 'GET'])
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
			myissue = collection.find(myquery)
			#print(ans)
			if myissue == None:
				ans = get_ans(k)
				i = {}
				i['url'] = k
				i['ans'] = ans
				collection.insert_one(i)
			else:
			 	ans = myissue['ans']
			if len(ans) > 0:
			 	return jsonify(ans)
			else:
			 	return jsonify({'error':'Similar Issues Not Found'})
			#for x in myissue:
			#	print(x)
	return {"url":ans}

if __name__ == "__main__":
    app.run(debug=True)