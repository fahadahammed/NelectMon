#  Copyright (c) Fahad Ahammed 2021. All rights reserved.
from src.library.redisops import RedisOps
import datetime
from src.library.fextras import byte_object_to_str
from src.library.password import PasswordManager


class User:
    def __init__(self):
        self.dt_now = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%s"))
        self.rc = RedisOps().rc

    def create_user(self, userObject):
        email = userObject.get("email")
        user_exists = self.get_user(email=email)
        if user_exists:
            return {"status": "error", "message": "User already exists"}
        new_user_object = {
            "email": userObject.get("email"),
            "name": userObject.get("name"),
            "password": PasswordManager().create_password(userObject.get("password")),
        }
        try:
            self.rc.hset(name=f"user:{email}", mapping=new_user_object)
            return {"status": "success", "message": "User created successfully"}
        except Exception as ex:
            return {"status": "error", "message": str(ex)}

    def get_user(self, email):
        try:
            the_user = self.rc.hgetall(name=f"user:{email}")
            the_user = byte_object_to_str(the_user)
            return the_user
        except Exception as ex:
            return {"status": "error", "message": str(ex)}

    def check_user_auth(self, email, password):
        user = self.get_user(email=email)
        password_ok = PasswordManager().check_password(plain_password=password, encrypted_password=user.get("password"))
        return password_ok
