from app.api.v1 import CsrfExemptAuth
from app.models import Home, HomeData
from rest_framework import (viewsets, serializers)
from app.common.enum_field_handler import EnumFieldSerializerMixin
from rest_framework.authentication import TokenAuthentication


class HomeSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'


class HomeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeData
        fields = '__all__'


class HomeViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptAuth.CsrfExemptSessionAuthentication, TokenAuthentication)
    serializer_class = HomeSerializer

    def get_queryset(self, **kwargs):
        queryset = Home.objects.filter(owner__user=self.request.user).order_by('id')
        return queryset


class HomeDataViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptAuth.CsrfExemptSessionAuthentication, TokenAuthentication)
    serializer_class = HomeDataSerializer

    def get_queryset(self, **kwargs):
        queryset = HomeData.objects.filter(home__owner__user=self.request.user).order_by('id')
        return queryset
