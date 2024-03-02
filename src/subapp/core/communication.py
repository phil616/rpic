import aiohttp
from conf import config
async def login_to_command_pod(session:aiohttp.ClientSession,url:str):
    login_payload = {
        "authcode":"hello",
        "ip":"",
        "port":""
    }

    port = 8000
    url = config.CP_HOST + ":" + str(port) + "/" + ""
    await session.post(url,data=login_payload)
    config.CP_HOST