//f4d33c9161a807f83e720022db389c264af9285e


const btnRepo = document.getElementById("btnRepos")
btnRepo.addEventListener("click", () => GetRepos())

const repolist = []
var c = 0

async function GetRepos(url = "https://api.github.com/search/repositories?q=stars:>-1") {
    const headers = {
        "Authorization" : "Token f4d33c9161a807f83e720022db389c264af9285e"
    }
    const response = await fetch(url, {
        "method" : "GET",
        "headers": headers
    })
    var result = await response.json()

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
        //console.log(repolist)
        const backheaders = {
            "Content-Type" : "application/json"
        }
        resfromback = await fetch ("http://localhost:3000", {
            "method" : "POST",
            "headers" : backheaders, 
            "body" : {
                "list" : repolist
            }
        })
        console.log(resfromback)
        return //we r on last page and we need to stop recursion
    }
    else {
        GetRepos(next)
    }

}
