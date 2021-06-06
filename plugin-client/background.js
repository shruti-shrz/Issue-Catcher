// crate popup to display the response from the backend.py
function createPopup(data, flag){  
var r = window.confirm("Do you want to see Similar Issues?"); // ask user whether he/she wants to see the similar issues or not
if(r == true) 
{
var popup = window.open("",'_blank',"toolbar=yes,scrollbars=yes,resizable=yes,top=100,left=500,width=500,height=300");
var t_txt = popup.document.createElement("div");
popup.document.body.style =  "background: #ADD8E6;" ;

if(flag) // Similar Issues found
{
    t_txt.innerHTML = "<strong><h2>Similar Issues</h2></strong>";
    popup.document.body.appendChild(t_txt);
    var ul_list = popup.document.createElement("UL");
    ul_list.setAttribute("id", "ullist");
    ul_list.style = "background: #FFFFFF;font-size:0px;"
    ul_list.innerHTML = data;
    popup.document.body.appendChild(ul_list);
    let menu = popup.document.getElementById('ullist');
    menu.removeChild(menu.lastElementChild);
}else{ // similar issues not found
    var no_issue = popup.document.createElement("div2");
    no_issue.innerHTML = "<strong><center><h2 style = \" font-size:20px;background: #FFFFFF; margin-top: 25px;\">"+data+"</h2></center></strong>";
    popup.document.body.appendChild(no_issue);
}

popup.document.title = "Similar Issues";
}

}

// take issue number from the content.js and sent to backend.py by making POST request
chrome.runtime.onMessage.addListener(function(response, sender, sendResponse){
console.log(response)
$.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5000/',
    dataType : 'json',
    data : response,
    success : function(data){ // on success get response from the backend
        var s = '';
        var d = JSON.parse(JSON.stringify(data))
        if(d.message) // No issue found
        {
            s = d.message;
            createPopup(s, false);
        }else // Similar Issue found
            {for(var i = 0; i < d.url.length; i++)
            {

                var h = d.url[i].url
                var l = "<li style = \"margin: 10px;font-size:15px;\"><a href =\""+h+"\" target=\"_blank\" rel=\"noopener noreferrer\">"+h+"</a><li>"
                s += l
            }
        createPopup(s, true);
        }
    },
    error: function (xhr, ajaxOptions, thrownError) { //Add these parameters to display the required response
        //alert(xhr.status);
        //alert(xhr.responseText);
       
    },
    });
})

