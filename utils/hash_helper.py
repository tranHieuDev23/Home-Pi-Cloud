import bcrypt


def hash(message):
    bcrypt.hashpw(message, bcrypt.gensalt(rounds=6))


def is_equal(message, hashed):
    bcrypt.checkpw(message, hashed)
