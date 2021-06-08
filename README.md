# IssueCatcher
![](images/rishalogo.png)   ![](images/iittplogo.png)

## What is IssueCatcher
IssueCatcher is a Chrome extension to help Github users find similar issues and pull requests to the issue they want to solve/explore. There are millions of issues out there on Github, and it is most likely for one to encounter an issue that has already been reported and discussed in some other repository and hence find solutions from these discussions that have happened under such similar issues. IssueCatcher provides list of top five similar issues and pull requests across Github to the input issue and speeds up the development process.

## Features of IssueCatcher
- Identifies the similar issues and pull requests across Github.
- After user clicks on an issue, confirmation pop up appears asking whether user wants to see similar issues or not and based on user input, displays list of five most similar issues and pull request links along with the similarity score.
- Issues' result, if already present in the database, gets updated by admin after every 15 days so that user gets an updated result.

## Working of IssueCatcher
The approach followed by IssueCatcher to detect similar issues and pull requests is summarised below.

![](images/issue.jpg)

- In current version, we have Chrome extension as the client-side and a Python backend.
- As soon as user clicks on an issue, issue url is sent to the backend (POST request).
- Then, we see if input issue is available in the database (MongoDB) or not, if issue is available in the database we directly fetch the result from the database and send to client-side to display.
- If issue is not available in the database, then we scrape input issue title and body and then using **LDA** model, generate the important technical keywords from the title of the input issue.
- The top four generated keywords from the previous step are used to make a query to the Github builtin search engine in order to get initial set of relevant issues.
- Then, we scrape the details of these issues (title, body) present in the first page (10 issues and pull requests) of the result from the previous step.
- Now, pretrained **Sentence BERT** model takes input issue title+body and that of each of the issues we got from the previous step as input and generate similarity score w.r.t. input issue.
- The previous 3 steps are repeated with the keywords from code snippets if they are present in the input issue's body.
- Based on similarity score, top five issues are send to the client-side as well as stored in the database.
- There is also an /admin route which takes GET requests and updates the issues in DB if the last update has been more than 15 days back.


## Snapshot of the UI
![](images/snapshotui.png)

Snapshot of the UI of IssueCatcher. As soon as user clicks on an issue, the confirm message appears as shown by [A]. If user clicks on **OK**, pop-up appears as shown by [B], displaying the top five similar issue and pull request links along with the Similarity Score.

## How to install IssueCatcher
- Clone this repository by typing following command in the Terminal
```
git clone https://github.com/shruti-shrz/Issue-Catcher.git
```
Or directly download this repository in your local system.
- Type **chrome://extensions/** in the chrome browser (you are now taken to the chrome extension page).
- Switch on the **Developer Mode**, by clicking on the button in the top right corner.
- Click on **Load unpacked**, now go to the *IssueCatcher* folder.
- Select the folder **plugin-client** inside the *IssueCatcher* folder and click open.
- Now, IssueCatcher plugin is installed and visible in the chrome extension page, so switch ON the plugin incase its not by clicking on the button in the bottom right corner.

## How to Use IssueCatcher
- Navigate to the Github Issue page.
- Click on any issue (open or close) and wait. The response may take maximum 2-3 minutes as NLP models take some computation time.
- A confirm pop-up will appear asking *Do you want to see Similar Issues?*, Click on Yes (in case popup doesn't come in this time, refresh the page and wait).
- A window will pop up, displaying list of similar issue and pull request links along with the similarity score.

## How to contribute to IssueCatcher
In case of any bug, feature improvisation or enhancement of the tool, please make a pull request or open an issue to discuss what you would like to change. In case of any query or suggestions please feel free to contact Shruti Priya (cs18b043@iitp.ac.in) or W Pranathi (cs18b045@iitp.ac.in) or Venigalla Akhila Sri Manasa (cs18m017@iitp.ac.in) or Dr. Sridhar Chimalakonda (ch@iittp.ac.in) of RISHA Lab, IIT Tirupati, India.

