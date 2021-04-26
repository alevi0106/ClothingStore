import logging
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sql.models import database, User
from src.validations import validate_password, validate_email, validate_phone
from src.authentication import verify_password, get_password_hash, create_access_token, extract_id_from_token

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

app = FastAPI()
app.state.database = database
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def startup() -> None:
    db = app.state.database
    if not db.is_connected:
        await db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    db = app.state.database
    if db.is_connected:
        await db.disconnect()


@app.post("/signup", response_model=User)
async def signup(user: User):
    validate_password(user.password)
    validate_email(user.email)
    validate_phone(user.phone)
    user.password = get_password_hash(user.password)
    await user.save()
    return user.dict(exclude={'password'})


@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.objects.get(username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/getusers")
async def get_user(username: str):
    return await User.objects.get(username=username)


async def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        id = extract_id_from_token(token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"},)
    return await User.objects.get(id=id)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


