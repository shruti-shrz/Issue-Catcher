console.log("hello");
console.log(window.location.href);
var url = window.location.href;
var flag =0;
// chrome.storage.sync.get('userurl', function(data){
// 	console.log(data);
// 	flag = 1;
// });
// if(flag==0)
// {
// 	chrome.storage.sync.set({'userurl': url}, function(){

// 		console.log("Saved!!!")
// 	});
	
// }

if(url.includes("issues"))
{
	var res = url.split("/");
	var l = res[res.length - 1]
	console.log(l)
	let isnum = /^\d+$/.test(l);
	if(isnum)
	{
		//chrome.storage.sync.set({'userissue': res[res.length - 1]}, function(){
		console.log("Issue Selected!!!")
		console.log(url);
		chrome.runtime.sendMessage({"issue":url});
	//});
	
	}
	
}

//#issue_47523_link
// let paragraphs = document.get(".issue");#issue_1_link
// for (elf of paragraphs){
// 	elf.style['background-color'] = '#FF00FF';
// }
