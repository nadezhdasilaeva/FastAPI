from typing import Annotated

import uvicorn
from fastapi import FastAPI, Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# from router import router
from routers.user import router as router_user
from routers.car import router as router_car
from routers.rent import router as router_rent


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="CarShare",
    version="0.0.1",
    headers='test'
)

app.include_router(router_user)
app.include_router(router_car)
app.include_router(router_rent)

@app.get('/mem')
def mem_rout():
    return

uvicorn.run(app, port=1488)
