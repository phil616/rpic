"""
precheck: data inject
04
"""

import unittest
from loguru import logger as log
from requests import get, post
from conf import BASEURL

payload_dict = {
    "username":None,
    "password":None,
    "grant_type":None,
    "scope":None,
    "client_id":None,
    "client_secret":None,
    "group_name":None
}

class BackendGroupUserAddTest(unittest.TestCase):
    def setUp(self) -> None:
        payload_dict.update({"username":"system","password":"system"})
        payload_dict.update({"group_name":"plain_user_group"})
        payload_dict.update({"scope":"PROCEDURE:ACCESS PROCEDURE:MODIFY PROCEDURE:ADMIN GROUP:CURD GROUP:ENDPOINT USER:CURD SYSTEM:HARDWARE"})
        login_system = post(BASEURL+"/authorization/token",data=payload_dict)
        """with group payload"""
        assert login_system.status_code,200
        self.system_header = {"Authorization":"Bearer "+login_system.json().get("access_token")}
        log.info(f"system login success login with header {self.system_header}")
        return super().setUp()
    @classmethod
    def setUpClass(self) -> None:
        log.info("logging in")
        

if __name__ == '__main__':
    unittest.main()