import furl

f = furl.furl("http://www.google.com/q?animal=dog&size=small")
f.add({"animal": "cat", "size": "medium"})
print(f)