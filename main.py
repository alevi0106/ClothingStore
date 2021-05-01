import logging
import uvicorn
from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, status, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sql.models import Product, database, User
from sql.dbaccess import get_confirmed_user, get_unconfirmed_user
from src.authentication import verify_password, get_password_hash, create_access_token, extract_id_from_token
from src.email_validation import sendemail
from src.settings import EMAIL_REGEX, PASSWORD_REGEX, PHONE_REGEX, DOMAIN_URL

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


@app.post("/signup", response_model=User, response_model_exclude={"password"})
async def signup(email: str = Form(..., regex=EMAIL_REGEX),
                 password_plain: str = Form(..., min_length=8, regex=PASSWORD_REGEX),
                 phone: str = Form(..., regex=PHONE_REGEX)):
    hashed_password = get_password_hash(password_plain)
    user = User(password=hashed_password, email=email, phone=phone)
    token = create_access_token(user.email, expires_minutes=10)
    confirmation_link = DOMAIN_URL.strip("/") + "/confirmaccount/" + token
    sendemail(user.email, confirmation_link)  # TODO: Should make it async
    await user.save()
    return user


@app.get("/confirmaccount/{token}", response_model_exclude={"password"})
async def confirm_account(token: str):
    email = extract_id_from_token(token)  # TODO:  Handle errors
    user = await get_unconfirmed_user(email)
    user.confirmed = True
    await user.save()
    return user


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_confirmed_user(form_data.username)
    verify_password(form_data.password, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)
    return await renew_access_token(user)


async def get_user_from_token(token: str = Depends(oauth2_scheme)):  # depends oauth2scheme verifies token
    try:
        email = extract_id_from_token(token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"},)
    return await get_confirmed_user(email)


@app.get("/getusers", response_model=User)
async def get_user(user: User = Depends(get_user_from_token)):
    """Meant for debugging. Will be removed later"""
    return user


@app.get("/refreshtoken")
async def renew_access_token(user: User = Depends(get_user)):
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/forgotpassword", response_model=User, response_model_exclude={"password"})
async def forgot_password(email: str = Form(...)):
    user = get_confirmed_user(email)
    user.confirmed = False
    confirmation_link = DOMAIN_URL.strip("/") + "/confirmaccount/" + token
    sendemail(user.email, confirmation_link)  # TODO: Should make it async
    await user.save()
    return user   


# TODO: admin login


@app.get("/products", response_model=Product)
async def get_products():
    return await Product.objects.limit(20).all()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/cart", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/product-details", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("product-details.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


