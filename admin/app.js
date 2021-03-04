const express = require("express");
const app = express();

const repolist = []
var c = 0



app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html")
})

app.post("/", function(req, res) {
    res.json(req.body)   
})

app.listen(3000, function() {
    console.log("Server running on port 3000")
})