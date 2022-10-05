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




<!-- with: -->
">onerror=alert(document.cookie)</img>');<!--
-->

<!-- or:  -->

 <img src="image.gif" onerror="myFunction()"> 

```