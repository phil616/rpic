import requests
import loguru

log = loguru.logger


URL = "http://127.0.0.1:8000"

def jwt_decode(token: str) -> dict:
    import jwt
    return jwt.decode(token, "randomkey", algorithms=['HS256'])

def test_login():
    response = requests.post(
        f"{URL}/login", data={"username": "test", "password": "test"}
    )
    log.debug(response.json())

if __name__ == "__main__":
    print(jwt_decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsInBlciI6WyJQUk9DRURVUkU6QUNDRVNTIl0sImdpZCI6MSwiZXhwIjoxNzA3MDk5NDQ0LCJpc3MiOiJSUElDUyBCYWNrZW5kIn0.2OfJXouq4OeeIB7S2acP3jeYmryuVpFctZQUgMYYgGc"))
    test_login()
