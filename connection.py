import bcrypt
def register(passw):
    pa=passw.encode('utf-8')
    salt=bcrypt.gensalt(rounds=15)
    hash=bcrypt.hashpw(pa,salt)
    return hash


if __name__ == "__main__":
    passw=""
    register(passw)