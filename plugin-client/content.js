console.log("hello");
console.log(window.location.href);
var url = window.location.href;
if(url.includes("issues"))
{
	var res = url.split("/");
	console.log(res[res.length - 1])
}
//#issue_47523_link
// let paragraphs = document.get(".issue");#issue_1_link
// for (elf of paragraphs){
// 	elf.style['background-color'] = '#FF00FF';
// }
