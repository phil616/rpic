"""
Laying for 1st, no precheck
"""

import unittest
from loguru import logger as log
from requests import get, post
import pymysql
from conf import BASEURL
DBCONFIG = {
    'host': 'localhost',  # 数据库主机地址
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'database': 'rpics',  # 数据库名
    'charset': 'utf8mb4',  # 字符编码
    'cursorclass': pymysql.cursors.DictCursor
}

def execute_sql(sql:str):
    connection = pymysql.connect(**DBCONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            log.info(f"EXECUTING SQL: {sql}")
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        # 关闭数据库连接
        connection.close()

class BackendDataInjectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        tables = ["user","group",'role_scope',"group_user"]
        for table in tables:
            execute_sql(f"DELETE FROM `{table}`;")


    def test_inject_system_user(self):
        resp = post(BASEURL+"/sql/statements",json={
            "statement":"INSERT INTO `rpics`.`user` (`username`, `password`, `user_info`, `user_status`, `user_roles`) VALUES ('system', 'system', '\{\}', 1, 'system')"
        })
        log.info("SYSTEM USER: username:system password:system scope:system")
        self.assertEqual(resp.status_code,200)

    def test_inject_admin_user(self):
        resp = post(BASEURL+"/sql/statements",json={
            "statement":"INSERT INTO `rpics`.`user` (`username`, `password`, `user_info`, `user_status`, `user_roles`) VALUES ('admin', 'admin', '\{\}', 1, 'admin')"
        })
        log.info("ADMIN USER: username:admin password:admin scope:admin")
        self.assertEqual(resp.status_code,200)

    def test_inject_creator_user(self):
        resp = post(BASEURL+"/sql/statements",json={
            "statement":"INSERT INTO `rpics`.`user` (`username`, `password`, `user_info`, `user_status`, `user_roles`) VALUES ('creator', 'creator', '\{\}', 1, 'creator')"
        })
        log.info("creator USER: username:creator password:creator scope:creator")
        self.assertEqual(resp.status_code,200)

    def test_inject_plain_user(self):
        resp = post(BASEURL+"/sql/statements",json={
            "statement":"INSERT INTO `rpics`.`user` (`username`, `password`, `user_info`, `user_status`, `user_roles`) VALUES ('user', 'user', '\{\}', 1, 'user')"
        })
        log.info("user USER: username:user password:user scope:user")
        self.assertEqual(resp.status_code,200)

    def test_inject_user_scope(self):
        endpoints = "/init/userscope"
        resp = get(BASEURL+endpoints)
        self.assertEqual(resp.status_code,200)

    def test_inject_add_group(self):
        ...

if __name__ == '__main__':
    unittest.main()