const express = require("express")
const fetch = require("node-fetch")
const mongoose = require("mongoose")
const repo = mongoose.model("repos");

function filter_two(repo, sel_repo) {
	if(repo.tags.length!=0 && sel_repo.tags.length!=0)
	for (j of sel_repo)
	{
		for(i of repo.tags){
		if (i==j)
			retunr 1;
		}
	}
	
    return 0;
} 

router.post("/filters")
