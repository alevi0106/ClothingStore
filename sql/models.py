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
        tablename = "Users"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)
    phone: str = ormar.String(min_length=10, max_length=10)
    confirmed: bool = ormar.Boolean(default=False)


class UserAddress(ormar.Model):
    class Meta:
        tablename = "UserAddress"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    address: str = ormar.Text()


class Admin(ormar.Model):
    class Meta:
        tablename = "Admins"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)


class Product(ormar.Model):
    class Meta:
        tablename = "Products"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255, unique=True)
    description: str = ormar.Text()
    price: float = ormar.Float()
    quantity: int = ormar.Integer()


class ProductImage(ormar.Model):
    class Meta:
        tablename = "ProductImages"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    product: Product = ormar.ForeignKey(Product, nullable=False)
    path: str = ormar.String(max_length=255)


class Cart(ormar.Model):
    class Meta:
        tablename = "Carts"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    product: Product = ormar.ForeignKey(Product, nullable=False)


class Category(ormar.Model):
    class Meta:
        tablename = "Categories"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=10)
    type: str = ormar.String(max_length=10)

class CategoryProductLink(ormar.Model):
    class Meta:
        tablename = "CategoryProductLink"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    category: Category = ormar.ForeignKey(Category, nullable=False)
    product: Product = ormar.ForeignKey(Product, nullable=False)


class Order(ormar.Model):
    class Meta:
        tablename = "Orders"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    product: Product = ormar.ForeignKey(Product, nullable=False)
    price: float = ormar.Float()
    quantity: int = ormar.Integer()


class Payment(ormar.Model):
    class Meta:
        tablename = "Payments"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    order: Order = ormar.ForeignKey(Order, nullable=False)


    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255, unique=True)
    description: str = ormar.Text()
    price: float = ormar.Float()
    quantity: int = ormar.Integer()


metadata.create_all(engine)
