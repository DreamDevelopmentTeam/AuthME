from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pymysql
import pymongo
import json
import configparser

import utils
import db

app = FastAPI()


# 定义异常处理器，处理找不到API的异常
@app.exception_handler(404)
async def not_found(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content=
                        utils.generate_json(404, "not found",None))


@app.get("/")
# 系统状态检测
async def root():
    return utils.generate_json(200, "OK", None)


# @app.get("/load")
# # 加载配置文件
# async def load_config():
#     global mysql_host, mysql_port, mysql_database, mysql_charset, mysql_user, mysql_passwd, mongodb_url
#     # 读取config目录下mysql目录下的mysql.ini文件
#     try:
#         config = configparser.ConfigParser()
#         # 读取mysql.ini文件中的配置
#         config.read("config/mysql/mysql.ini")
#         mysql_host = config.get("mysql", "host")
#         mysql_port = config.get("mysql", "port")
#         mysql_database = config.get("mysql", "database")
#         mysql_charset = config.get("mysql", "charset")
#         mysql_user = config.get("mysql", "user")
#         mysql_passwd = config.get("mysql", "passwd")
#         # 读取config目录下mongodb目录下的mongodb.ini文件
#         config.read("config/mongodb/mongodb.ini")
#         mongodb_url = config.get("mongodb", "url")
#         return utils.generate_json(500, "Config load success", None)
#     except:
#         # 加载失败时显示
#         return utils.generate_json(500, "Config load failed", None)


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#

@app.get("/test/mysql")
# MYSQL数据库测试
async def test_mysql():
    # 连接mysql数据库
    try:
        db.get_mysql()
        return 'mysql ok'
    except:
        return 'mysql error'


@app.get("/test/mongodb")
# MONGODB数据库测试
async def test_mongodb():
    # 连接mongodb数据库
    try:
        client = db.get_mongo()
        print(client.list_database_names())
        test_db = client["test_db"]
        return 'mongodb ok'
    except:
        return 'mongodb error'




@app.post('/login')
# 登录
async def login(username: str = "", password: str = ""):#,database: str = "mysql"
    if username == "" or password == "":
        return utils.generate_json(400,"Invalid parameter",None)
    try:
        # 连接mysql数据库
        dbc = db.get_mysql()
        # 创建游标
        cursor = dbc.cursor()
        # 执行SQL语句
        cursor.execute("SELECT * FROM `user` WHERE `username` = '" + username + "' AND `password` = '" + password + "'")
        # 获取所有记录列表
        results = cursor.fetchall()
        # 关闭数据库连接
        # db.close()
        # 判断是否有数据
        if len(results) > 0:
            # 有数据，登录成功
            return utils.generate_json(200, "Login success", None)
        else:
            # 无数据，登录失败
            return utils.generate_json(500, "Login failed", None)
    except Exception as ex:
        pass