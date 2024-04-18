import datetime
from sqlmodel import Field, SQLModel, create_engine, Relationship, UniqueConstraint
import uuid


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)

    id: uuid.UUID = Field(primary_key=True, default=None)
    password: str = Field(min_length=64, max_length=64)  # хэш пароля
    role: str  # роль пользователя
    email: str  # почта
    first_name: str  # имя
    last_name: str  # отчество
    surname: str  # фамилия
    license: str = Field(min_length=10, max_length=10)  # права
    date_reg: datetime.datetime  # дата регистрации

    rents: list['Rent'] = Relationship(back_populates='users')
    payments: list['Payment'] = Relationship(back_populates='users')



class Car(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("car_number"),)

    id: uuid.UUID = Field(primary_key=True, default=None)
    brand: str  # марка авто
    model: str  # модель авто
    latitude: float  # широта
    longitude: float  # долгота
    car_number: str  # гос_номер
    price_order: int  # цена аренды

    rents: list['Rent'] = Relationship(back_populates='cars')


class Rent(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default=None)
    id_user: uuid.UUID = Field(default=None, foreign_key='user.id')  # id_пользователя
    car_id: uuid.UUID = Field(default=None, foreign_key='car.id')
    data_rent_start: datetime.datetime  # дата аренды начало
    data_rent_end: datetime.datetime = None     # дата аренды конец
    status: str     # 'continues' или 'end'

    users: list['User'] = Relationship(back_populates='rents')
    payments: list['Payment'] = Relationship(back_populates='rents')
    cars: list['Car'] = Relationship(back_populates='rents')


class Payment(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default=None)
    id_rent: uuid.UUID = Field(default=None, foreign_key='rent.id')  # id_аренды
    id_user: uuid.UUID = Field(default=None, foreign_key='user.id')  # id_пользователя
    cart_number: str  # последние 4 цифры карты
    data: datetime.datetime  # дата оплаты

    rents: list['Rent'] = Relationship(back_populates='payments')
    users: list['User'] = Relationship(back_populates='payments')

class UserUpdate(SQLModel):
    email: str
    password: str


sqlite_file_name = "../database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)