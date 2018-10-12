function my_ajax(url, success_callback, fail_callback= null, method="get", params=null, async=true) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
                success_callback(xmlhttp)
            } else if (xmlhttp.status == 500 || xmlhttp.status == 404) {
                fail_callback(xmlhttp)
            }
        }
    }

    xmlhttp.open(method, url, async)
    if (method=="post"){
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    }

    xmlhttp.send(params)
}




// function my_ajax(obj) {
//     var xmlhttp;
//     if (window.XMLHttpRequest) {
//         xmlhttp = new XMLHttpRequest();
//     }
//     else {
//         xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//     }
//     xmlhttp.onreadystatechange = function () {
//         if (xmlhttp.readyState == 4) {
//             if (xmlhttp.status == 200) {
//                 success_callback(xmlhttp)
//             } else if (xmlhttp.status == 500 || xmlhttp.status == 404) {
//                 fail_callback(xmlhttp)
//             }
//         }
//     }
//
//     xmlhttp.open(obj["method"], url, async)
//     if (method=="post"){
//         xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
//     }
//
//     xmlhttp.send(params)
// }
//
// my_ajax({
//     "url":"xx",
//     "method":"get"
// })