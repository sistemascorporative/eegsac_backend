from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class EstadoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoExamen
        fields = '__all__'


class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'


class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'


class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = '__all__'


class RespuestaExamenProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaExamenPrograma
        fields = '__all__'


class RespuestaExamenCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaExamenCurso
        fields = '__all__'


class RegistroExamenProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroExamenPrograma
        fields = '__all__'


class RegistroExamenCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroExamenCurso
        fields = '__all__'
