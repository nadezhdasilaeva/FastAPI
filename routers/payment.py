import uuid

from fastapi import APIRouter, HTTPException
from database.DataBase_def import get_payments, get_payment, make_payment

router = APIRouter(prefix='/payment',
                   tags=['payment'],
                   responses={404: {"description": "Not found"}})


@router.get('/all')
def get_payments_rout():
    return get_payments()


@router.get('/{payment_id}')
def get_payment_rout(payment_id: uuid.UUID):
    return get_payment(payment_id)


@router.post('/make/{user_id}')
def make_payment_rout(user_id: uuid.UUID, rent_id: uuid.UUID, cart_number: str):
    return make_payment(user_id, rent_id, cart_number)
