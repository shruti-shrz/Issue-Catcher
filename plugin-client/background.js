chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
console.log(response)
$.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5000/',
    type: 'POST',
    dataType : 'json',
    data : response,
    success: function (newArticle){
       alert('success');
    }
    });

	alert(response)
    sendResponse({ message: "Background has received that message" });
})