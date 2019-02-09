$(document).ready(function (){

    chrome.tabs.getSelected(null,function(tab){
        var link = document.createElement('a');
        link.href = tab.url;
        var u = link.toString();
        $.post("http://127.0.0.1:5000/api",{
        url:u
    },function(data,status){
        $('#host').html(data.toString());
        
    });
        // $('#host').html(u);
    })
})


// $("#player-container").innerHTML = "A"
// document.getElementById("#player-container").innerHTML = "A"
