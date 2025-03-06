import pymysql

# 数据库连接参数
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '10086',
    'database': 'study',
    'charset': 'utf8mb4',
}

# SQL 执行器
def con_my_sql(sql_code):
    connection = pymysql.connect(**DB_CONFIG)
    connection.ping(reconnect=True)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql_code)
        connection.commit()
        return cursor  # 返回游标对象，调用者负责关闭
    except pymysql.MySQLError as error_message:
        connection.rollback()
        print(f"MySQL Error: {error_message}")
        return None
    finally:
        # 不在这里关闭连接，交由调用者负责
        pass


