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


