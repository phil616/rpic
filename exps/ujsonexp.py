import ujson

r = ujson.dumps({'a': 1, 'b': 2},indent=4)
print(r)
print(r.__repr__())

ori = '{"a":1,"b":2}'
print(ori.__repr__())
s = ujson.loads(ori)
print(s)