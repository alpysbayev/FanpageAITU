from sqlalchemy.orm import Session
import schemas
import models
import hashlib


def hash_password(password):
    hash_pass = hashlib.md5(password.encode())
    return hash_pass.hexdigest()
