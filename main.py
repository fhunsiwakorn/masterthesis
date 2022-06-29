from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users as rtu
from routers import patients as rtpt
from routers import prediction as rtpdt
from routers import master_data as rtmtd
from routers import dashboard as rtdb
from tortoise.contrib.fastapi import register_tortoise
# from tortoise.functions import Avg, Count, Sum


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def config_router1():
    app.include_router(rtu.router)


def config_router2():
    app.include_router(rtpt.router)


def config_router3():
    app.include_router(rtpdt.router)


def config_router4():
    app.include_router(rtmtd.router)


def config_router5():
    app.include_router(rtdb.router)


config_router1()
config_router2()
config_router3()
config_router4()
config_router5()

register_tortoise(
    app,
    # db_url="postgres://postgres:siw@k0rn@localhost:5432/thesis",
    db_url="postgres://otwqywzqjukrkz:f39ee5684cd5b5d9080b21f328137c0898beb6634fd29a901952749bb63439a0@ec2-44-198-82-71.compute-1.amazonaws.com:5432/d665kv1713jh6i",
    modules={"models": ["models.user", "models.patient"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
# mysql://root:@127.0.0.1:3306/quart
