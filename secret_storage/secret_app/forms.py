from django import forms
from secret_app.models import Secret
from secret_app.utils import generate_key, create_lifetime, aes_encryptor
import hashlib

DEGREE_BASE = 16


class CreateSecretForm(forms.Form):
    secret_word = forms.CharField(
        max_length=128,
    )
    secret_text = forms.CharField(
        max_length=1000,
    )

    def __init__(self, *args, **kwargs):
        self._microseconds = None
        self._seconds = None
        self._days = None
        super(CreateSecretForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        self._microseconds = self.data['timedelta']['microseconds']
        self._seconds = self.data['timedelta']['seconds']
        self._days = self.data['timedelta']['days']

        if not type(self._microseconds) is int:
            raise forms.ValidationError("Invalid microseconds type")

        if not type(self._seconds) is int:
            raise forms.ValidationError("Invalid seconds type")

        if not type(self._days) is int:
            raise forms.ValidationError("Invalid days type")

        if not 0 <= self._microseconds < 1000000:
            raise forms.ValidationError("Invalid microseconds value")

        if not 0 <= self._seconds < 86400:
            raise forms.ValidationError("Invalid seconds value")

        if not 0 <= self._days < 999999999:
            raise forms.ValidationError("Invalid days value")

        return cleaned_data

    def save(self, *args, **kwargs):
        cleaned_data = super().clean()
        text_secret = cleaned_data.get('secret_text')
        text_word = cleaned_data.get('secret_word')

        bytes_word = bytes(text_word, 'utf-8')
        hash_word = hashlib.md5(bytes_word).hexdigest()

        string_to_cipher = text_secret + ' ' * (DEGREE_BASE - (len(text_secret) % DEGREE_BASE))
        encryptor = aes_encryptor(text_word)
        ciphertext = encryptor.encrypt(string_to_cipher)

        secret = Secret(secret_text=ciphertext, secret_word=hash_word)
        key = generate_key()
        secret.secret_key = key

        secret.lifetime = create_lifetime(days=self._days,
                                          seconds=self._seconds,
                                          microsec=self._microseconds
                                          )

        secret.save()

        return secret
