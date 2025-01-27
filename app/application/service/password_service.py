import logging
import string
import random

from argon2 import PasswordHasher

ph = PasswordHasher()
JWT_ALGORITHM = 'HS256'

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    return ph.hash(password=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception as e:
        logger.error(e)
        return False


def gen_otp(otp_length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=otp_length))
