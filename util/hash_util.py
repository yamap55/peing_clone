import hashlib
import random


def calculate_password_hash(password: str, salt: str) -> str:
    text = (password + salt).encode('utf-8')
    result = hashlib.sha512(text).hexdigest()
    return result


DIGITS_AND_ALPHABETS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def create_salt(digit_num=50) -> str:
        return "".join(random.sample(DIGITS_AND_ALPHABETS, digit_num))


def compare_password(password: str, password_hash: str, salt: str):
    p = calculate_password_hash(password, salt)
    return p == password_hash
