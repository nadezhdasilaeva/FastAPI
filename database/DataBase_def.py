import uuid
from passlib.hash import pbkdf2_sha256
import datetime

from fastapi import HTTPException, Response

from database.DataBase_model import User, Car, Rent, engine, Payment
from sqlmodel import SQLModel, Session, select

from internal.crypto import create_jwt_token, create_cookie


def create_table():
    SQLModel.metadata.create_all(engine)


def hash_password_f(password: str):
    return pbkdf2_sha256.hash(password)


def check_password(hash_password: str, hash: str):
    return pbkdf2_sha256.verify(hash_password, hash)



def get_users():
    with Session(engine) as session:
        return session.exec(select(User).where(User.role == 'user')).all()

def get_user_by_email(email: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email)).first()


def get_temp_users():
    with Session(engine) as session:
        return session.exec(select(User).where(User.role == 'temp_user')).all()


def get_user(user_id: uuid.UUID):
    with Session(engine) as session:
        if not session.exec(select(User).where(User.id == user_id)).first():
            raise HTTPException(status_code=404, detail="User not found")
        return session.exec(select(User).where(User.id == user_id)).first()


def check_user(email: str, password: str, response: Response):
    with Session(engine) as session:
        user_data = select(User).where(User.email == email)
        user = session.exec(user_data).first()
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        if not check_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        jwt_token = create_jwt_token({'id': str(user.id), 'email': user.email, 'role': user.role})
        create_cookie(response, jwt_token)
        raise HTTPException(status_code=200)


def delete_user(user_id: uuid.UUID):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        raise HTTPException(status_code=200)


def reg_user(email: str,
             password: str,
             first_name: str,
             last_name: str,
             surname: str,
             license: str):
    user = User(id=uuid.uuid4(),
                email=email,
                password=hash_password_f(password),
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                date_reg=datetime.datetime.utcnow(),
                role='temp_user',
                license=license
                )
    with Session(engine) as session:
        if session.exec(select(User).where(User.email == email)).first() is None:
            session.add(user)
            session.commit()
            raise HTTPException(status_code=200)
        else:
            raise HTTPException(status_code=400, detail="Email is busy")


def verify_user(user_id: uuid.UUID):
    with Session(engine) as session:
        results = session.exec(select(User).where(User.id == user_id))
        user = results.one()

        user.role = 'user'
        session.add(user)
        session.commit()
        session.refresh(user)
        raise HTTPException(status_code=200)


def update_user_email(user_id: uuid.UUID, new_email: str, password: str):
    hash_password = hash_password_f(password)
    with Session(engine) as session:
        if session.exec(select(User).where(User.email == new_email)).first():
            raise HTTPException(status_code=400, detail='Email is busy')
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if hash_password != user.password:
            raise HTTPException(status_code=400, detail='Incorrect password')
        user.sqlmodel_update({'email': new_email})
        session.add(user)
        session.commit()
        session.refresh()
        return user


def update_user_password(user_id: uuid.UUID, email: str, new_password: str, new_password_2: str):
    if new_password != new_password_2:
        raise HTTPException(status_code=400, detail="Incorrect password")
    hash_password = hash_password_f(new_password)
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if email != user.email:
            raise HTTPException(status_code=400, detail='Incorrect email')
        user.sqlmodel_update({'email': email})
        session.add(user)
        session.commit()
        session.refresh()
        return user


def get_all_car():
    with Session(engine) as session:
        return session.exec(select(Car)).all()


def get_car(car_id: uuid.UUID):
    with Session(engine) as session:
        if not session.exec(select(Car).where(Car.id == car_id)).first():
            raise HTTPException(status_code=404, detail="Car not found")
        return session.exec(select(Car).where(Car.id == car_id)).first()


def add_car(brand: str,
            model: str,
            latitude: float,
            longitude: float,
            car_number: str,
            price_order: int):
    car = Car(id=uuid.uuid4(),
              brand=brand,
              model=model,
              latitude=latitude,
              longitude=longitude,
              car_number=car_number,
              price_order=price_order)
    with Session(engine) as session:
        session.add(car)
        session.commit()
        raise HTTPException(status_code=200)


def delete_car(car_id: uuid.UUID):
    with Session(engine) as session:
        session.delete(session.exec(select(Car).where(Car.id == car_id)).first())
        session.commit()
        raise HTTPException(status_code=200)


def get_rents():
    with Session(engine) as session:
        return session.exec(select(Rent)).all()


def get_rent(rent_id: uuid.UUID):
    with Session(engine) as session:
        return session.exec(select(Rent).where(Rent.id == rent_id)).first()


def start_rent(user_id: uuid.UUID, car_id: uuid.UUID):
    rent = Rent(id=uuid.uuid4(),
                user_id=user_id,
                car_id=car_id,
                data_rent_start=datetime.datetime.utcnow(),
                status='continues')
    with Session(engine) as session:
        session.add(rent)
        session.commit()
        raise HTTPException(status_code=200)


def end_rent(rent_id: uuid.UUID):
    with Session(engine) as session:
        rent = session.exec(select(Rent).where(Rent.id == rent_id)).one()
        rent.data_rent_end = datetime.datetime.utcnow()
        rent.status = 'end'

        session.add(rent)
        session.commit()
        raise HTTPException(status_code=200)



def get_payments():
    with Session(engine) as session:
        return session.exec(select(Payment)).all()


def get_payment(payment_id):
    with Session(engine) as session:
        return session.exec(select(Payment).where(Payment.id == payment_id)).first()


def make_payment(user_id: uuid.UUID, rent_id: uuid.UUID, cart_number):
    payment = Payment(id=uuid.uuid4(),
                      user_id=user_id,
                      rent_id=rent_id,
                      cart_number=cart_number,
                      data=datetime.datetime.utcnow()
                      )
    with Session(engine) as session:
        session.add(payment)
        session.commit()
        raise HTTPException(status_code=200)
# create_table()