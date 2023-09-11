from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import pymysql
import pymongo
import json

import utils

app = FastAPI()

# 定义异常处理器，处理找不到API的异常
@app.exception_handler(404)
async def not_found(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"message": "not found"})


@app.get("/")
async def root():
    return utils.generate_json(200, "OK", None)

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#

@app.get("/test/mysql")
async def test_mysql():
