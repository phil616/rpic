"""
NOT Finished 
"""
import rpyc
from rpyc import connect
from rpyc.utils.authenticators import SSLAuthenticator
def magic_word_authenticator(sock):
    if sock.recv(5) != "abcde":
        raise AuthenticationError("wrong magic word")
    return sock, None
conn = connect("localhost", 18861, authenticator=SSLAuthenticator(magic_word_authenticator))
conn = rpyc.connect("localhost", 18861, config=config)
result = conn.root.exposed_add(10, 20)
print("Result:", result)
conn.close()