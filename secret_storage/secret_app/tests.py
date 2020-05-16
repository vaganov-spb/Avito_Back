from django.test import TestCase, Client
from secret_app.factories import SecretFactory
import factory
import hashlib
from datetime import timedelta
from secret_app.utils import aes_encrypt
from faker import Factory
import json
import random
import string
import sys

# coverage run --omit='*/venv/*' manage.py test --keepdb


faker = Factory.create()


MAX_MICROSEC_VALUE = 999999
MAX_SECONDS_VALUE = 86399
MAX_DAYS_VALUE = 999999998
MAX_TEXT = 1000
MAX_WORD = 128


def string_generator(size=128, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def create_response(microsec, seconds, days, text, phrase):
    return {
        "data": {
            "type": "Secret",
            "attributes": {
                "timedelta": {
                    "microseconds": microsec,
                    "seconds": seconds,
                    "days": days
                },
                "secret_text": text,
                "secret_word": phrase
            }
        }
    }


class CreateSecret(TestCase):
    def setUp(self):
        self.client = Client()
        self.microseconds = random.randint(1, MAX_MICROSEC_VALUE)
        self.seconds = random.randint(1, MAX_SECONDS_VALUE)
        self.days = random.randint(1, MAX_DAYS_VALUE)
        self.text_size = random.randint(1, MAX_TEXT)
        self.word_size = random.randint(1, MAX_WORD)
        self.text = string_generator(self.text_size)
        self.phrase = string_generator(self.word_size)

    def test_create_valid_secret(self):
        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_microseconds_value(self):
        self.microseconds = random.randint(MAX_MICROSEC_VALUE, sys.maxsize)

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['__all__'], ['Invalid microseconds value'])
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_microseconds_type(self):
        self.microseconds = string_generator()

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['__all__'], ['Invalid microseconds type'])
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_seconds_value(self):
        self.seconds = random.randint(MAX_SECONDS_VALUE, sys.maxsize)

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['__all__'], ['Invalid seconds value'])
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_seconds_type(self):
        self.seconds = string_generator()

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['__all__'], ['Invalid seconds type'])
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_days_value(self):
        self.days = random.randint(MAX_DAYS_VALUE, sys.maxsize)

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['__all__'], ['Invalid days value'])
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_days_type(self):
        self.days = string_generator()

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['__all__'], ['Invalid days type'])
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_phrase_size(self):
        self.phrase = string_generator(size=2 * MAX_WORD)

        data = create_response(self.microseconds, self.seconds, self.days, self.text, self.phrase)
        response = self.client.post('/generate/', data=data, content_type='application/vnd.api+json')
        content = json.loads(response.content)

        self.assertEqual(content['errors']['secret_word'], ['Ensure this value has at most 128 characters (it has 256).'])      #noqa
        self.assertEqual(response.status_code, 400)


class GetSecret(TestCase):
    def setUp(self):
        self.client = Client()
        self.word = faker.word()[:128]
        self.text = faker.text()[:1000]
        self.secret = SecretFactory()
        self.secret.secret_text = aes_encrypt(self.text, self.word)
        self.secret.secret_word = hashlib.md5(self.word.encode()).hexdigest()

    def test_get_valid_secret(self):
        self.secret.lifetime = timedelta(days=1)
        self.secret.save()

        response = self.client.post(
            f"/secret/{self.secret.secret_key}/",
            content_type='application/vnd.api+json',
            data={
                "data": {
                    "type": "Secret",
                    "attributes": {
                        "secret_word": self.word
                    }
                }
            })
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['data'], self.text)

    def test_get_already_read_secret(self):
        self.secret.lifetime = timedelta(days=1)
        self.secret.is_read = True
        self.secret.save()

        response = self.client.post(
            f"/secret/{self.secret.secret_key}/",
            content_type='application/vnd.api+json',
            data={
                "data": {
                    "type": "Secret",
                    "attributes": {
                        "secret_word": self.word
                    }
                }
            })
        self.assertEqual(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEqual(content['errors'], 'You have already read this secret')

    def test_get_timeout_secret(self):
        self.secret.lifetime = timedelta(microseconds=1)
        self.secret.save()

        response = self.client.post(
            f"/secret/{self.secret.secret_key}/",
            content_type='application/vnd.api+json',
            data={
                "data": {
                    "type": "Secret",
                    "attributes": {
                        "secret_word": self.word
                    }
                }
            })
        self.assertEqual(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEqual(content['errors'], 'Lifetime of your secret is over')

    def test_get_non_existing_secret(self):
        self.secret.lifetime = timedelta(days=1)
        self.secret.save()

        response = self.client.post(
            f"/secret/{self.secret.secret_key[::-1]}/",
            content_type='application/vnd.api+json',
            data={
                "data": {
                    "type": "Secret",
                    "attributes": {
                        "secret_word": self.word
                    }
                }
            })
        self.assertEqual(response.status_code, 404)

    def test_get_incorrect_phrase(self):
        self.secret.lifetime = timedelta(days=1)
        self.secret.save()

        response = self.client.post(
            f"/secret/{self.secret.secret_key}/",
            content_type='application/vnd.api+json',
            data={
                "data": {
                    "type": "Secret",
                    "attributes": {
                        "secret_word": self.word[::-1]
                    }
                }
            })
        self.assertEqual(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEqual(content['errors'], 'Your code phrase is invalid')


