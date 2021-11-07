from passlib.hash import pbkdf2_sha256, bcrypt_sha256


class PasswordManager:
    def __init__(self):
        self.plain_password = None
        self.encrypted_password = None

    def create_password(self, plain_password):
        self.plain_password = plain_password
        self.encrypted_password = pbkdf2_sha256.encrypt(self.plain_password, rounds=200000, salt_size=16)
        return self.encrypted_password

    def check_password(self, plain_password, encrypted_password):
        self.plain_password = plain_password
        self.encrypted_password = encrypted_password
        try:
            checkp = pbkdf2_sha256.verify(self.plain_password, self.encrypted_password)
            print(checkp)
            return pbkdf2_sha256.verify(self.plain_password, self.encrypted_password)
        except Exception as ex:
            return False

    def bcrypt_create_password(self, plain_password):
        self.plain_password = plain_password
        self.encrypted_password = bcrypt_sha256.encrypt(self.plain_password, rounds=10, salt_size=22)
        return self.encrypted_password

    def bcrypt_check_password(self, plain_password, encrypted_password):
        self.plain_password = plain_password
        self.encrypted_password = encrypted_password
        if bcrypt_sha256.verify(self.plain_password, self.encrypted_password):
            return True
        else:
            return False
