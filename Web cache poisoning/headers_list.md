Identified parameter on a850006040a4dc5c0fb6750008500a2.web-security-academy.net:

# origin
indicates the origin (scheme, hostname, and port) that caused the request. For example, if a user agent needs to request resources included in a page, or fetched by scripts that it executes, then the origin of the page may be included in the request. 

**syntax**
```
Origin: null
Origin: <scheme>://<hostname>
Origin: <scheme>://<hostname>:<port>
```


# x-forwarded-host
de-facto standard header for identifying the originating IP address of a client connecting to a web server through a proxy server.

de-facto standard header for identifying the original host requested by the client in the Host HTTP request header. 

 Host names and ports of reverse proxies (load balancers, CDNs) may differ from the origin server handling the request, in that case the X-Forwarded-Host header is useful to determine which Host was originally used.

This header is used for debugging, statistics, and generating location-dependent content and by design it exposes privacy sensitive information, such as the IP address of the client. Therefore the user's privacy must be kept in mind when deploying this header.

A standardized version of this header is the HTTP Forwarded header.

**syntax**
```
X-Forwarded-Host: <host>

```


# x-original-url
represents the original header value received in **HttpContext.Connection** and **HttpContext.Request** When using Nginx/IIS/Apache to setup a reverse proxy.

the original **HttpContext.Request.Scheme** will be saved as header **X-Original-Proto: ...,** 

the **HttpContext.Request.Scheme** will be changed to the left-most scheme in the header of **X-Forwarded-Proto: o1, o2, ...**

the original **HttpContext.Request.Host** will be saved as header **X-Original-Host: <original-host>**, 

 **HttpContext.Request.Host** will be changed to the left-most host in the header of **X-Forwarded-Host: o1, o2, ...**

the original **HttpContext.Connection.RemoteIpAddress** and **HttpContext.Connection.RemotePort** will be saved as header **OriginalForHeaderName: <original-endpoint>**, and then this value will be changed to left-most IP and port in header of **X-Forwarded-For: o1, o2, ...**


# sec-websocket-version
Request header

Specifies the WebSocket protocol version the client wishes to use, so the server can confirm whether or not that version is supported on its end.


