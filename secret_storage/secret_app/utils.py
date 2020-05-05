from secret_app.models import Secret
import uuid
import datetime
from Crypto.Cipher import AES
import hashlib

IV = 16 * '\x00'
MODE = AES.MODE_CBC


def create_lifetime(days, seconds,  microsec):
    return datetime.timedelta(
        days=days,
        seconds=seconds,
        microseconds=microsec
    )


def aes_encryptor(text_key):
    sha_base = bytes(text_key, 'utf-8')
    sha_key = hashlib.sha256(sha_base)
    sha_key = sha_key.digest()
    encryptor = AES.new(sha_key, MODE, IV=IV)
    return encryptor


def generate_key():
    flag = False
    uuid_key = None
    secret_key = None
    while not flag:
        uuid_key = uuid.uuid4().hex
        secret_key = prettier_uuid(uuid_key)
        flag = valid_key(secret_key)
    return secret_key


def prettier_uuid(uuid_str):
    prettier_key = uuid_str.replace('-', '')
    return prettier_key.lower()


def valid_key(key):
    try:
        secret = Secret.objects.get(secret_key=key)
        return False
    except Secret.DoesNotExist:
        return True
