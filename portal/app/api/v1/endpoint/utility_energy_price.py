from app.models import UtilityEnergyPrice
from rest_framework import (viewsets, serializers)


class UtilityEnergyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityEnergyPrice


class UtilityEnergyPriceViewSet(viewsets.ModelViewSet):
    serializer_class = UtilityEnergyPrice
    queryset = UtilityEnergyPrice.objects.all()