from django.shortcuts import render
from secret_app.models import Secret
from secret_app.serializers import SecretSerializer
from rest_framework import viewsets


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
