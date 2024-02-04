from pymysql import connect


def execute_mysql_query(sql_query: str) -> None:
    with connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        port=3306,
        database="RPICS"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            conn.commit()

def insert_fake_data():
    user_SQL = "INSERT INTO USER (username,password,user_info,user_roles,user_status) VALUES ('user','user','{\"test\": \"test\"}','user',1);"
    admin_SQL = "INSERT INTO USER (username,password,user_info,user_roles,user_status) VALUES ('admin','admin','{\"test\": \"test\"}','admin',1);"
    creator_SQL = "INSERT INTO USER (username,password,user_info,user_roles,user_status) VALUES ('creator','creator','{\"test\": \"test\"}','creator',1);"
    system_SQL = "INSERT INTO USER (username,password,user_info,user_roles,user_status) VALUES ('system','system','{\"test\": \"test\"}','system',1);"
    
    execute_mysql_query(user_SQL)
    execute_mysql_query(admin_SQL)
    execute_mysql_query(creator_SQL)
    execute_mysql_query(system_SQL)
    