import socket

hostname = "www.google.com"
ip_addr = socket.gethostbyname(hostname)
print(ip_addr)
