BASEURL = "http://localhost:8000"
TOKEN_FILE = "token.txt"
STR2TOLE = {
    "admin-管理员":"admin",
    "user-普通用户":"user", 
    "creator-创建者":"creator",
    "system-系统管理员":"system"
}
ROLE2SCOPE = {
    "user":"PROCEDURE:ACCESS",
    "creator":"PROCEDURE:MODIFY",
    "admin":"PROCEDURE:ADMIN GROUP:CURD GROUP:ENDPOINT USER:CURD",
    "system":"PROCEDURE:ACCESS PROCEDURE:MODIFY PROCEDURE:ADMIN GROUP:CURD GROUP:ENDPOINT USER:CURD SYSTEM:HARDWARE"
}
# a mapping from annotation to role
