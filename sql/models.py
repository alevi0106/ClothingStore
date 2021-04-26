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
    username: str = ormar.String(max_length=255, unique=True)
    password: str = ormar.String(max_length=255)
    email: str = ormar.String(max_length=255, unique=True)
    phone: str = ormar.String(min_length=10, max_length=10)


metadata.create_all(engine)
