import httpx




r = httpx.Client()
n = r.get("https://www.baidu.com",timeout=3)
print(n.status_code)