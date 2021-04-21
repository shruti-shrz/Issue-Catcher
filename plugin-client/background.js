// Example POST method implementation:
// async function postData(url = '', data = {}) {
//   // Default options are marked with *
//   const response = await fetch(url, {
//     method: 'POST', // *GET, POST, PUT, DELETE, etc.
//     mode: 'cors', // no-cors, *cors, same-origin
//     cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
//     credentials: 'same-origin', // include, *same-origin, omit
//     headers: {
//       'Content-Type': 'application/json'
//       // 'Content-Type': 'application/x-www-form-urlencoded',
//     },
//     redirect: 'follow', // manual, *follow, error
//     referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
//     body: JSON.stringify(data) // body data type must match "Content-Type" header
//   });
//   return response.json(); // parses JSON response into native JavaScript objects
// }

function createPopup(data){
    
var r = window.confirm("Do you want to see Similar Issues?");
if(r == true)
{
var popup = window.open("",'_blank',"toolbar=yes,scrollbars=yes,resizable=yes,top=100,left=500,width=500,height=300");
//popup.onload = function() { this.document.title = "your new title"; }

var t_txt = popup.document.createElement("div");
var ul_list = popup.document.createElement("UL");
ul_list.setAttribute("id", "ullist");
popup.document.body.style =  "background: #ff9999;" ;
t_txt.innerHTML = "<strong><h2>Similar Issues</h2></strong>";
popup.document.body.appendChild(t_txt);
ul_list.style = "background: #ffe5e5; padding: 20px;"
ul_list.innerHTML = data;
popup.document.body.appendChild(ul_list);
let menu = popup.document.getElementById('ullist');
menu.removeChild(menu.lastElementChild);
popup.document.title = "Similar Issues";
}

}


chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
console.log(response)
// postData('http://127.0.0.1:5000/',response).then(data => {
//     console.log(data); // JSON data parsed by `data.json()` call
//   });
$.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5000/',
    dataType : 'json',
    data : response,
    success : function(data){
        var s = '';
        var d = JSON.parse(JSON.stringify(data))
        //alert(d);
        //alert(d.url)
        for(var i = 0; i < d.url.length; i++)
        {

            var h = d.url[i].url
            var l = "<li style = \"margin-left: 20px;font-size:15px;\"><a href =\""+h+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+h+"</a><li>"
            s += l
        }
        //s+="<ol>"
       // alert(s)
       //  h = data["url"][0]["url"]
       // var s = ["<a href="+h+">"+h+"</a>","<a href=www.google.com>www.google.com</a>"]
       createPopup(s);
       //alert("heyy")

    },
    error: function (xhr, ajaxOptions, thrownError) { //Add these parameters to display the required response
        alert(xhr.status);
        alert(xhr.responseText);
       
    },
    });
	// alert(response)
 //    sendResponse({ message: "Background has received that message" });
 // .done(function (data){
 //        console.log(`background's response: ${data.response}`);
 //       #sendResponse({message:data.response})
 //    }).fail(function (error){
 //        console.log(`error: ${error}`);
 //        #sendResponse({"error":error})
 //    })

})

