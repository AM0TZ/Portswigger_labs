# OAuth 2.0 authentication vulnerabilities
https://portswigger.net/web-security/oauth

# OAuth grant types
https://portswigger.net/web-security/oauth/grant-types


# 1. Lab: Authentication bypass via OAuth implicit flow
https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow

 To solve the lab, log in to Carlos's account. His email address is carlos@carlos-montoya.net. 

log-in via:
 wiener:peter

 GET /auth
 ?
 client_id=sb46hqyhw713x55hrqce3
 redirect_uri=https://0af8002a031f1e3ac0824cac00a7003a.web-security-academy.net/oauth-callback
 response_type=token
 nonce=605756732
 scope=openid%20profile%20email 
 HTTP/1.1



# 2. Lab: Forced OAuth profile linking
https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking

To solve the lab, use a CSRF attack to attach your own social media profile to the admin user's account on the blog website, then access the admin panel and delete Carlos. 

cred:
    Blog website account: wiener:peter
    Social media profile: peter.wiener:hotdog
