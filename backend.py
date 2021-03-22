#import pymongo
#from pymongo import MongoClient
from flask import Flask
from flask import request
from issueParser import *
#cluster =  MongoClient("")
#db = cluster["githubRepos"]
#collection = db["repos_issues"]
k = "hello"
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def bootstrap():
	global k
	if request.method == 'POST':
		if not request.form:
			print("nothing!!!")
		else:
			var = request.form
			k = var['issue']
			print(k,type(k))
			get_ans(k)
			#myquery = {"issue_number":"test"}
			#myissue = collection.find(myquery)
			#for x in myissue:
			#	print(x)
	return k

if __name__ == "__main__":
    app.run(debug=True)