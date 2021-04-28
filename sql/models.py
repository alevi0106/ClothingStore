import ormar
import sqlalchemy
import databases
from typing import Optional

from src.settings import DATABASE_URL


metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
database = databases.Database(DATABASE_URL)


class User(ormar.Model):
    class Meta:
        tablename = "users"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)
    phone: str = ormar.String(min_length=10, max_length=10)


class Product(ormar.Model):
    class Meta:
        tablename = "products"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255, unique=True)
    description: str = ormar.Text()
    price: float = ormar.Float()
    quantity: int = ormar.Integer()


class Cart(ormar.Model):
    class Meta:
        tablename = "carts"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    userid: User = ormar.ForeignKey(User)


metadata.create_all(engine)
