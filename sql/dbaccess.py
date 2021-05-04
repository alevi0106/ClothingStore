from sql.models import User


async def get_confirmed_user(email: str) -> User:
    return await User.objects.filter((User.confirmed == True) & (User.email == email)).get()


async def get_unconfirmed_user(email: str) -> User:
    return await User.objects.filter((User.confirmed == False) & (User.email == email)).get()


async def get_admin_user(email: str) -> User:
    return await User.objects.filter((User.confirmed == True) & (User.email == email)).select_related("admins").get()
