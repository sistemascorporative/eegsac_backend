from rest_framework import serializers
from .models import *


# Define los serializers para cada modelo

class CredencialProgramaMatriculadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredencialProgramaMatriculado
        fields = '__all__'


class CredencialProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredencialPrograma
        fields = '__all__'


class CertificadoCursoMatriculadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoCursoMatriculado
        fields = '__all__'


class CertificadoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoCurso
        fields = '__all__'

