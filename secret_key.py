import os
import base64


def get_or_create_secret_key(filename="secret_key.txt"):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return file.read()
    else:
        # Generate a new secret key
        secret_key = base64.b64encode(os.urandom(32))
        with open(filename, "wb") as file:
            file.write(secret_key)
        return secret_key


SECRET_KEY = get_or_create_secret_key()
