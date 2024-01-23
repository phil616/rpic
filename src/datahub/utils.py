from uuid import uuid4
import bcrypt
import datetime
import aiofiles

async def a_write_file(path: str, content: bytes):
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)
        await f.flush()
        await f.close()  # not necessary if using async with

async def a_read_file(path: str) -> bytes:
    async with aiofiles.open(path, "rb") as f:
        return await f.read()
    
def write_file(path: str, content: bytes):
    with open(path, "wb") as f:
        f.write(content)
        f.flush()
        f.close()  # not necessary if using keyword `with`

def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def generate_uuid():
    return str(uuid4()).replace("-", "")

def generate_password_hash(password):
    if isinstance(password,str):
        password = password.encode("utf-8")
    return str(bcrypt.hashpw(password,bcrypt.gensalt()))[2:-1]

def verify_password(password,hashed_password):
    if isinstance(password,str):
        password = password.encode("utf-8")
    if isinstance(hashed_password,str):
        hashed_password = hashed_password.encode("utf-8")
    if bcrypt.checkpw(password,hashed_password):
        return True
    else:
        return False


def get_boot_time():
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return str(time_now)
