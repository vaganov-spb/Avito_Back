from rest_framework_json_api import serializers
from secret_app.models import Secret


class SecretSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Secret
        fields = ('secret_key', 'secret_text', 'secret_word', 'added_at', 'lifetime')
