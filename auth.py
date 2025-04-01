import bcrypt
from database import insert_user, get_user_by_email

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def register(username, email, password, descriptor_blob=None):
    hashed = hash_password(password)
    insert_user(username, email, hashed, descriptor_blob)

def login(email, password):
    user = get_user_by_email(email)
    if user and verify_password(password, user[3]):
        return True, user
    return False, None
