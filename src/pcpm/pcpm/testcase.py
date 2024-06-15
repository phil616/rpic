"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

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