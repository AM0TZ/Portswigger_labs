# ***Lab: Discovering vulnerabilities quickly with targeted scanning***
https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing/lab-discovering-vulnerabilities-quickly-with-targeted-scanning

 This lab contains a vulnerability that enables you to read arbitrary files from the server. To solve the lab, retrieve the contents of /etc/passwd within 10 minutes.

Due to the tight time limit, we recommend using Burp Scanner to help you. You can obviously scan the entire site to identify the vulnerability, but this might not leave you enough time to solve the lab. Instead, use your intuition to identify endpoints that are likely to be vulnerable, then try running a targeted scan on a specific request. Once Burp Scanner has identified an attack vector, you can use your own expertise to find a way to exploit it. 


check the **POST /product/stock HTTP/1.1** with active scan:
see alert:
```
Issue:  XML injection
Severity:  Medium
Confidence:  Certain
Host:  https://0abb00b604db2803c01044fc00f300ca.web-security-academy.net
  
Issue detail:
2 instances of this issue were identified, at the following locations:
/product/stock [productId parameter]
/product/stock [storeId parameter]
```
