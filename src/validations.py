import re


re_pass = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
re_email = re.compile("^([a-z0-9]+@[a-z0-9]+\.[a-z]+)$")


def validate_password(plain_password: str):
    if not re_pass.match(plain_password):
        raise ValueError("Password improper")
    return plain_password


def validate_email(email: str):
    if not re_email.match(email):
        raise ValueError("Improper Email")
    return email


def validate_phone(phone: str):
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Improper phone number")
    return phone
