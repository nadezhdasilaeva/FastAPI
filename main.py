from typing import Annotated

import uvicorn
from fastapi import FastAPI, Cookie, Depends
from fastapi.security import OAuth2PasswordBearer

# from router import router
from routers.user import router_user
from routers.car import router_car


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="CarShare",
    version="0.0.1",
    headers='test'
)

app.include_router(router_user)
app.include_router(router_car)


uvicorn.run(app, port=8001)
