import uuid
from passlib.hash import pbkdf2_sha256
import datetime

from fastapi import HTTPException, Response

from database.DataBase_model import User, Car, engine, UserUpdate
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
        return 200


def delete_user(user_id: uuid.UUID):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()

        session.delete(user)
        session.commit()
        return 200


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
            return 200
        else:
            return {'This email is already in use'}


def verify_user(user_id: uuid.UUID):
    with Session(engine) as session:
        results = session.exec(select(User).where(User.id == user_id))
        user = results.one()

        user.role = 'user'
        session.add(user)
        session.commit()
        session.refresh(user)
        return 200


def update_user(user_id: uuid.UUID, user: UserUpdate):
    user.password = hash_password_f(user.password)
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        print(db_user)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        print(db_user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def get_all_car():
    with Session(engine) as session:
        return session.exec(select(Car)).all()


def get_car(car_id: uuid.UUID):
    with Session(engine) as session:
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
        return 200


def delete_car(car_id: uuid.UUID):
    with Session(engine) as session:
        session.delete(session.exec(select(Car).where(Car.id == car_id)).first())
        session.commit()
        return 200

