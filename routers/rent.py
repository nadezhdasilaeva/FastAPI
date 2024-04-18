import uuid

from fastapi import APIRouter, HTTPException
from database.DataBase_def import get_rents, get_rent, end_rent, start_rent

router = APIRouter(prefix='/rent',
                   tags=['rent'],
                   responses={404: {"description": "Not found"}})

@router.get('/all')
def get_rents_rout():
    return get_rents()


@router.get('/{rent_id}')
def get_rent_rout(rent_id):
    return get_rent(rent_id)


@router.post('/start_rent')
def start_rent_rout(user_id: uuid.UUID, car_id: uuid.UUID):
    return start_rent(user_id, car_id)


@router.post('/end_rent')
def end_rent_rout(rent_id: uuid.UUID):
    return end_rent(rent_id)