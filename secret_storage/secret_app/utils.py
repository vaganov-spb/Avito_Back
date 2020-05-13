from secret_app.models import Secret
import uuid
import base64
import datetime
from Crypto.Cipher import AES
from Crypto import Random
import hashlib

MODE = AES.MODE_CBC


def create_lifetime(days, seconds,  microsec):
    return datetime.timedelta(
        days=days,
        seconds=seconds,
        microseconds=microsec
    )


def aes_encrypt(text, key):
    sha_key = hashlib.sha256(key.encode()).digest()
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(sha_key, MODE, IV=IV)
    text = text + (AES.block_size - len(text) % AES.block_size) * ' '
    return base64.b64encode(IV + encryptor.encrypt(text.encode()))


def aes_decrypt(enc, key):
    sha_key = hashlib.sha256(key.encode()).digest()
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(sha_key, AES.MODE_CBC, iv)
    return cipher.decrypt(enc[AES.block_size:]).decode('utf-8')


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

