from secret_app.models import Secret
import uuid
import datetime


def create_lifetime(days, seconds,  microsec):
    return datetime.timedelta(
        days=days,
        seconds=seconds,
        microseconds=microsec
    )


def string_lifetime_repr(days, seconds,  microsec):
    return str(days) + ':' + str(seconds) + ':' + str(microsec)


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
