def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, # this is just a protocol:domain:port string like https://example.com:443
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False,
                           maxQueueSize=10,
                           timeout=5,
                           maxRetriesPerRequest=3,
                           autoStart=False
                           )

    # We have to call engine.start() manually because we disabled autoStart
    engine.start(timeout=5)

def login_process(req, interesting):
    if 'name="csrf" value="' in req.response:
         = 


    login1a = """GET /login HTTP/1.1
Host: 0a16004204188226c0aa3517009a008c.web-security-academy.net
Connection: close

"""








    engine.queue(oddRequest)

    for word in open('/usr/share/dict/words'):
        engine.queue(target.req, word.rstrip())
        
        

def handleResponse(req, interesting):
    if '404 Not Found' not in req.response:
        table.add(req)
