import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
from issueParser import *
from flask_cors import CORS
cluster =  MongoClient("mongodb://pranshru:MaYln5lrN8EobbxbYZeOPHat9sIyvTX7bo6LZAgNizerY9soW7TnjdATsWuzThZGlZZB0oAaerXO0lIvSnjyiA==@pranshru.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@pranshru@")
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