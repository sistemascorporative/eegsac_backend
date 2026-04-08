from rest_framework import serializers
from core.models import EstadoRegistro

class EstadoRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoRegistro
        fields = '__all__'