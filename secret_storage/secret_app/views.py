from secret_app.models import Secret
from secret_app.serializers import SecretSerializer, CreateSecretSerializer
from rest_framework.decorators import action
from secret_app.forms import CreateSecretForm
from rest_framework.response import Response
from rest_framework import viewsets, status


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer


class CreateSecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = CreateSecretSerializer

    @action(methods=['post'], detail=False, url_path='generate')
    def CreateSecret(self, request):
        form = CreateSecretForm(request.data)
        if form.is_valid():
            secret = form.save()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(secret, many=False)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response({'detail': form.errors}, status.HTTP_400_BAD_REQUEST)
