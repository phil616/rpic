import socket

def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

ip = get_ip()
print("IP地址:", ip)