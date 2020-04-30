from django import forms
from secret_app.models import Secret
from secret_app.utils import generate_key, string_lifetime_repr


class CreateSecretForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._microseconds = None
        self._seconds = None
        self._days = None
        super(CreateSecretForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CreateSecretForm, self).clean()
        self._microseconds = self.data['timedelta']['microseconds']
        self._seconds = self.data['timedelta']['seconds']
        self._days = self.data['timedelta']['days']

        if not 0 <= self._microseconds < 1000000:
            self.add_error('microseconds', 'Invalid microseconds value')

        if not 0 <= self._seconds < 86400:
            self.add_error('seconds', 'Invalid seconds value')

        if not 0 <= self._days < 999999999:
            self.add_error('days', 'Invalid days value')

        return cleaned_data

    def save(self, *args, **kwargs):
        cleaned_data = super(CreateSecretForm, self).clean()
        text = cleaned_data['secret_text']
        word = cleaned_data['secret_word']
        secret = Secret(secret_text=text, secret_word=word)
        key = generate_key()
        secret.secret_key = key
        secret.lifetime = string_lifetime_repr(
            self._days,
            self._seconds,
            self._microseconds
        )
        secret.save()
        return secret

    class Meta:
        model = Secret
        fields = ['secret_text', 'secret_word']
