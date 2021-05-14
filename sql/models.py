import ormar
import sqlalchemy
import databases

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
    confirmed: bool = ormar.Boolean(default=False)


class UserAddress(ormar.Model):
    class Meta:
        tablename = "useraddress"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    address: str = ormar.Text()


class Admin(ormar.Model):
    class Meta:
        tablename = "admins"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)


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


class ProductImage(ormar.Model):
    class Meta:
        tablename = "productimages"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    product: Product = ormar.ForeignKey(Product)
    path: str = ormar.String(max_length=255, unique=True)
    sequence: int = ormar.Integer(default=1)  # Sequence 0 will be thumbnail
    image_tag: str = ormar.String(max_length=10, default="img")


class Cart(ormar.Model):
    class Meta:
        tablename = "carts"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    product: Product = ormar.ForeignKey(Product, nullable=False)


class Category(ormar.Model):
    class Meta:
        tablename = "categories"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    products = ormar.ManyToMany(Product, nullable=True)
    name: str = ormar.String(max_length=10, unique=True)
    categorytype: str = ormar.String(max_length=10)


class Order(ormar.Model):
    class Meta:
        tablename = "orders"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    product: Product = ormar.ForeignKey(Product, nullable=False)
    price: float = ormar.Float()
    quantity: int = ormar.Integer()


class Payment(ormar.Model):
    class Meta:
        tablename = "payments"
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
