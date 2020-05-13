from secret_app.models import Secret
from secret_app.utils import aes_decrypt
from secret_app.serializers import SecretSerializer, CreateSecretSerializer
from rest_framework.decorators import action
from secret_app.forms import CreateSecretForm
from rest_framework.response import Response
from rest_framework import viewsets, status
import hashlib
from django.utils import timezone


class CreateSecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = CreateSecretSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        form = CreateSecretForm(request.data)
        if form.is_valid():
            secret = form.save()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(secret, many=False)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response({'detail': form.errors}, status.HTTP_400_BAD_REQUEST)


class GetSecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = CreateSecretSerializer
    http_method_names = ['post']

    def create(self, request,  *args, **kwargs):
        return Response('Create function is not offered in this path', status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=False, url_path='(?P<secret_key>[0-9a-f]{32})')
    def GetSecret(self, request, secret_key):
        secret_word = request.data['secret_word']
        try:
            secret = Secret.objects.get(secret_key=secret_key)
        except Secret.DoesNotExist:
            return Response('Invalid secret key', status.HTTP_404_NOT_FOUND)
        except Secret.MultipleObjectsReturned:
            return Response('There are more than 1 secret with such key', status.HTTP_300_MULTIPLE_CHOICES)

        if secret.added_at + secret.lifetime < timezone.now():
            return Response('Lifetime of your secret is over', status.HTTP_403_FORBIDDEN)

        if secret.is_read:
            return Response('You have already read this secret', status.HTTP_403_FORBIDDEN)

        bytes_word = bytes(secret_word, 'utf-8')
        hash_word = hashlib.md5(bytes_word).hexdigest()

        if hash_word != secret.secret_word:
            return Response('Your code phrase is invalid', status.HTTP_403_FORBIDDEN)
        else:
            data = aes_decrypt(secret.secret_text, secret_word)
            secret.is_read = True
            secret.save()
            return Response(data.rstrip(), status.HTTP_200_OK)
