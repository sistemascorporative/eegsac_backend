from rest_framework import serializers
from .models import MatriculaPrograma, MatriculaCurso
from rest_framework import serializers


class MatriculaProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatriculaPrograma
        fields = '__all__'


class MatriculaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatriculaCurso
        fields = '__all__'