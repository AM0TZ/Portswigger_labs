def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=1000,
                           engine=Engine.BURP, # Use Burp's HTTP/1 network stack, including upstream proxies etc. You can also use Engine.BURP2 for HTTP/2.
                           pipeline=False
                           )

    for pin in range(0,9999):
        guess = str(pin).zfill(4)
        engine.queue(target.req, guess)


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status != 404:
        table.add(req)
