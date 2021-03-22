const express = require("express")
const fetch = require("node-fetch")
const mongoose = require("mongoose")
const github_topics = require("github-topics")

require("dotenv").config()
const app = express()
const mongo_pass = process.env.MONGO_PASS

const MONGOURI = `mongodb+srv://pinky:${mongo_pass}@cluster0.hfcw3.mongodb.net/IssueCatcherDB?retryWrites=true&w=majority`
mongoose.connect(MONGOURI,{
    useNewUrlParser: true,
    useUnifiedTopology: true,
	useFindAndModify: false
});

mongoose.connection.on('connected',()=>{
   console.log("We are connected")
});
mongoose.connection.on('error',(err)=>{
   console.log("Error in connection",err)
});

require('./repo')
const Repo = mongoose.model("Repo")

const api_key = process.env.API_KEY
const repolang_key = process.env.REPOLANG_KEY
const issue_key = process.env.ISSUE_KEY

var repolist = []
var c = 0

const headers = {
    "Authorization" : `Token ${api_key}`
}

const repolang_headers = {
    "Authorization" : `Token ${repolang_key}`
}


const issue_headers = {
    "Authorization" : `Token ${issue_key}`
}
//20*C + 25*CI + 15*OI + 20*P + 20*S
function formula(repo) {
    return 0.20 * repo.forks_count + 0.20 * repo.open_issues_count + 0.20 * repo.stargazers_count;
} 

async function GetRepos(url = "https://api.github.com/search/repositories?q=stars:>-1") {
    
    var response = await fetch(url, {
        "method" : "GET",
        "headers": headers
    })
    var result = await response.json()
    //console.log(response);
    await result.items.forEach(async repo => {
        var repolang = await fetch(repo.languages_url, {
            "method" : "GET",
            "headers" : repolang_headers
        })
        var lang = await repolang.json()
        const score = formula(repo)
        const topics = github_topics.gettopics(repo.html_url);
        const repo_new = new Repo({
            name: repo.full_name,
            stargazers_count: repo.stargazers_count,
            forks_count: repo.forks_count,
            open_issues_count: repo.open_issues_count,
            score: score,
            languages: Object.keys(lang),
            about: repo.description,
            tags: topics
        });
        //repolist.push(repo_new);
        await repo_new.save();
    });
    console.log("Inserted Batch " + c);
    //console.log(repolist);
    // try {
    //     const insres = await Repo.insertMany(repolist);
    //     console.log(insres + " to insert" + c);
    //     repolist = []
    // } catch(err) {
    //     console.log(err);
    // }

    var link = response.headers.get("link")
    var links = link.split(",")
    var next = ""
    var last = ""
    links.forEach(a => {
        elts = a.split(";")
        if (elts[1].includes("next")){
            next = elts[0].replace("<","").replace(">","")
        }
        else if(elts[1].includes("last")) {
            last = elts[0].replace("<","").replace(">","")
        }
    });
    c = c + 1
    if(next == "") {
        return //we r on last page and we need to stop recursion
    }
    else {
        await GetRepos(next)
    }

}

app.get("/", async function(req, res) {
    await GetRepos()
    res.status(200).json({repolist})
    
    // .catch(function(err) {
    //     res.json({err})
    // })
       
})

app.listen(3000, function() {
    console.log("Server running on port 3000")
})