import bcrypt


def hash_message(message: str):
    return bcrypt.hashpw(message.encode(), bcrypt.gensalt(rounds=6)).decode()


def is_equal(message: str, hashed: str):
    return bcrypt.checkpw(message.encode(), hashed.encode())
