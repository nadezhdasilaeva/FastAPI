import uuid

from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database.DataBase_def import get_users, get_temp_users, get_user, check_user, delete_user, reg_user, verify_user, update_user_emil
from database.DataBase_model import UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router_user = APIRouter(prefix='/user',
                        tags=['user'],
                        responses={404: {"description": "Not found"}})


@router_user.get('/all')
def get_users_rout():
    return get_users()


@router_user.get('/temp_users')
def get_temp_users_rout():
    return get_temp_users()


@router_user.get('/{user_id}')
def get_user_rout(user_id: uuid.UUID):
    return get_user(user_id)


@router_user.post('/sing_in')
def check_user_rout(email: str, password: str):
    return check_user(email, password)


@router_user.delete('/del/')
def delete_user_rout(user_id: uuid.UUID):
    return delete_user(user_id)

@router_user.post('/reg')
def reg_user_rout(email: str,
             password: str,
             first_name: str,
             last_name: str,
             surname: str,
             license: str):
    return reg_user(email, password, first_name, last_name, surname, license)


@router_user.put('/verify/{user_id}')
def verify_user_rout(user_id: uuid.UUID):
    return verify_user(user_id)


@router_user.put('/update/{user_id}')
def update_user_email_rout(user_id: uuid.UUID, email: str, password: str):
    return update_user_emil(user_id, email, password)

