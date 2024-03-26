from serialize import serializer,deserializer
from compile import assemble_cp39,disassemble_cp39,exec_object
from crypto import encrypt,decrypt
from codex import encode,decode

def f(r: int) -> int:
    print(r**2)
    def inner():
        print(r**3)
    return inner

f(4)
cp39_object = assemble_cp39(f,[4])
cp39_bytes = serializer(cp39_object)
cp39_encode = encode(cp39_bytes)
cp39_encrypt = encrypt(cp39_encode)
print(cp39_encrypt)
r_cp39_decrypt = decrypt(cp39_encrypt)
r_cp39_decode = decode(r_cp39_decrypt)
r_cp39_bytes = deserializer(r_cp39_decode)
r_cp39_object = disassemble_cp39(r_cp39_bytes)
exec_object(r_cp39_bytes)()