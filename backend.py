import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request, jsonify
from issueParser import *
cluster =  MongoClient("")
db = cluster['IssueDB']
collection = db['issues']
k = "hello"
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bootstrap():
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
			ans = []
			if myissue == None:
				ans = get_ans(k)
				i = {'url' : k, 'ans': ans}
				collection.insert_one(i)
			else:
				ans = myissue['ans']
			if len(ans) > 0:
				return jsonify(ans)
			else:
				return jsonify({'error':'Similar Issues Not Found'})
			#for x in myissue:
			#	print(x)

if __name__ == "__main__":
    app.run(debug=True)