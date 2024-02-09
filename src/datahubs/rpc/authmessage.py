"""
Structures for the authentication message

1. message header
start with 4 bytes of magic word: b'RPIC'
2. message body
1024-4-4=1016 bytes of username and password
3. message footer
end with 4 bytes of magic word: b'RPIC'

if body is wider than 1016 bytes, it will be truncated
"""

