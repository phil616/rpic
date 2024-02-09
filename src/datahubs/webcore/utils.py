import aiohttp
import jwt
async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
def decrypt_jwt(token: str, key: str, algorithm: str):
    return jwt.decode(token, key, algorithms=algorithm)