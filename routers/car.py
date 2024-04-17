import uuid

from fastapi import APIRouter

from database.DataBase_def import get_all_car, add_car, get_car, delete_car

router_car = APIRouter(prefix='/car',
                       tags=['car'],
                       responses={404: {"description": "Not found"}})


@router_car.get('/all')
def get_all_car_rout():
    return get_all_car()



@router_car.get('/{car_id}')
def get_car_rout(car_id: uuid.UUID):
    return get_car(car_id)


@router_car.post('/add_car')
def add_car_rout(brand: str,
            model: str,
            latitude: float,
            longitude: float,
            car_number: str,
            price_order: int):
    return add_car(brand, model,latitude, longitude, car_number, price_order)


@router_car.delete('/delete')
def delete_car_rout(car_id: uuid.UUID):
    return delete_car(car_id)


# @router_car.put('/update')
# def update_car(car_id: uuid.UUID):
