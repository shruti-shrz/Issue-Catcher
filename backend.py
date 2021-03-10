import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import request
cluster =  MongoClient("mongodb+srv://Shruti:Er8LXanOea3vbiTD@cluster0.x6sds.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["githubRepos"]
collection = db["repos_issues"]
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
			myquery = {"issue_number":"test"}
			myissue = collection.find(myquery)
			for x in myissue:
				print(x)
	return k
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, World!"
if __name__ == "__main__":
    app.run(debug=True)