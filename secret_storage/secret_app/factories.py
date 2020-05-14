import factory
import uuid
from faker import Factory
from secret_app.models import Secret

faker = Factory.create()


class SecretFactory(factory.DjangoModelFactory):
    class Meta:
        model = Secret

    secret_key = faker.uuid4().lower().replace('-', '')

