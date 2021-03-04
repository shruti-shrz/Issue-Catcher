const express = require("express");
const fetch = require("node-fetch")
require("dotenv").config()
const app = express();
const api_key = process.env.API_KEY

var repolist = []
var c = 0

async function GetRepos(url = "https://api.github.com/search/repositories?q=stars:>-1") {
    const headers = {
        "Authorization" : `Token ${api_key}`
    }
    var response = await fetch(url, {
        "method" : "GET",
        "headers": headers
    })
    var result = await response.json()
    //console.log(response);
    result.items.forEach(repo => {
        repolist.push(repo.url)
    });
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
    if(next == "" || c == 2) {
        return //we r on last page and we need to stop recursion
    }
    else {
        GetRepos(next)
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