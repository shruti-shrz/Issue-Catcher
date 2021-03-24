import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
from issueParser import *
from flask_cors import CORS
from settings import MONGOPASS
cluster =  MongoClient('mongodb://pinky:'+MONGOPASS+'@cluster0-shard-00-00.hfcw3.mongodb.net:27017,cluster0-shard-00-01.hfcw3.mongodb.net:27017,cluster0-shard-00-02.hfcw3.mongodb.net:27017/IssueDB?ssl=true&replicaSet=atlas-10ak0x-shard-0&authSource=admin&retryWrites=true&w=majority')
#db = cluster['IssueDB']
collection = cluster['issues']
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
				collection.insert_one(i)
			else:
				print("Picked from db!")
				ans = myissue['ans']
				print(ans)
			if len(ans) > 0:
			 	return jsonify({'url' : ans})
			else:
			 	return jsonify({'error':'Similar Issues Not Found'})
	return jsonify({'url' : ans})

if __name__ == "__main__":
    app.run(debug=True)