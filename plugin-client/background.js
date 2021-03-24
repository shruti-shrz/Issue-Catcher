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
var popup = open("", "Popup", "width=300,height=200");
var txtOk = popup.document.createElement("div");
var aOk = popup.document.createElement("a");
txtOk.innerHTML = "<strong><h2>Similar Issues</h2></strong>";
popup.document.body.appendChild(txtOk);
    aOk.innerHTML = aOk.innerHTML + data + "<br />";
    popup.document.body.appendChild(aOk);
 


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
        var s = [];
        int k=0;
        for(i in data["url"])
        {
           var h = i[k]['url']
            var l = "<a href="+h+">"+h+"</a>"
            s.push(l)
            k++
        }
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

