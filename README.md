# Issue-Catcher

This is a tool to help github users find issues and pull requests similar to the issue they want to solve/explore. There are millions of issues out there, and it is most likely for one to find an issue that has already been pointed out and discussed about in some repository, that is very similar or possibly the same issue that you are facing, and hence can get solutions from these discussions that have happened under such similar issues. Hence, we hope this tool will be widely used by fellow developers and evolves greatly through contributions.

## How to run/use this tool
### Installations
* Ensure you have Python 3.7 installed in your computer.
* Clone this repository and run the following in the terminal if you don't already have these libraries installed:
```
pip3 install pymongo
pip3 install flask
pip3 install flask_cors
pip3 install threading
pip3 install datetime
pip3 install gensim
pip3 install nltk
pip3 install numpy
pip3 install re
pip3 install pandas
pip3 install requests
pip3 install json
pip3 install bs4
pip3 install sklearn
pip3 install sentence_transformers
```
* Run the following in python command line interface:
```
import nltk
nltk.download('stopwords')
```
* After this, create an account in MongoDB and paste the genarted key in **backend.py** inside MongoClient. 
* Rename the file **settings_template.py** as **settings.py** and copy-paste your MongoDB password as mantioned below:
```
MONGOPASS = "password"
```
### The Run
* To get the backend running, you have to navigate to the ```Issue-Catcher``` directory and run the following in the terminal:
```
python3 backend.py
```
* To get the extension, go to **Google Chrome** and navigate to the ```chrome://extensions``` page and switch ON Developer Mode. Click on the button ```Load unpacked``` and select the ```Issue-Catcher/plugin-client``` folder. You will see **Github_plugin** under the list of extensions and you can switch that ON now.
* Now, to see the tool in action! navigate to any issue from any repository, ensure backend is running and extension is ON, reload the issue if there's no change in the terminal running backend.
* You will get a pop-up asking if you want to see similar issues. Press OK and this will give you a Chrome window displaying links to the similar issues found. If not, you will get a pop-up notifying that no similar issues were found, sorry!

## About the tool
* The extension, when switched ON, gets the URL the user is currently browsing, and if it is a Github Issue URL, it is passed on to the backend through a POST request asking for similar issues.
* In the backend, the title, body, labels and other useful details of the input issue are scraped with the help of **BeautifulSoup**. 
* The **LDA** model is used to extract keywords from the title of the input issue, and these are used to query for Github issues.
* The top 20 issues are scraped, their details are obtained, and a similarity score is got w.r.t. the input issue for each of these 20 (or less) issues using a **BERT** similarity model.
* Another thread in the backend simultaneously runs a search for issues having some of the same code the input issue has, and these are also given a similairty score.
* Finally top 5 issues' URLs are returned and displayed for user. 
* These issues and their similar issues are stored in a **MongoDB** Atlas database, so if some input issue is already there in the DB, the links are directly returned from DB.
* There is a feature, which scraps other issues in the current repository user is in, in the background and fills up the DB with issues and their similar ones, so as to speed up response next time. To see how this works, kindly uncomment the appropriate code in ```backend.py```
* There is also an /admin route which takes GET requests and updates the issues in DB if the last update has been more than 15 days back.


