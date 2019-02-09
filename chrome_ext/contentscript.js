// from 
// https://stackoverflow.com/questions/34077641/how-to-detect-page-navigation-on-youtube-and-modify-html-before-page-is-rendered
window.addEventListener("spfdone", process); // old youtube design
window.addEventListener("yt-navigate-start", process); // new youtube design
document.addEventListener("DOMContentLoaded", process); // one-time early processing
// window.addEventListener("load", process); // one-time late postprocessing 



function process() {
    // console.log("into porcess!");
    $.post("http://127.0.0.1:5000/api",{
        url:document.URL
    },function(data,status){
        var d = data;
        console.log(d);
        if (d == '1'){
            document.body.innerHTML = "<h1>Elsa Gate Detect!</h1>";   
        }
    });
}