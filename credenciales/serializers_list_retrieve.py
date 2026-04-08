from rest_framework import serializers
from .models import *
from aula.serializers import ProgramaSerializer
from aula.serializers_list_retrieve import *
from users.serializers_list_retrieve import EstudianteUserSerializerList, UserSimpleSerializerList
from matriculas.serializers_list_retrieve import MatriculaProgramaSerializerList, MatriculaCursoSerializerList


# Define los serializers para cada modelo

class CredencialProgramaMatriculadoSerializerList(serializers.ModelSerializer):
    crepromatprocod = MatriculaProgramaSerializerList()
    class Meta:
        model = CredencialProgramaMatriculado
        fields = [
            "creprocod",
            "creprofecemi",
            "creprofeccad",
            "creprocer",
            "creprodip",
            "creprocarnet",
            "crepromatprocod",
        ]


class CredencialProgramaSerializerList(serializers.ModelSerializer):
    creproestcod = UserSimpleSerializerList()
    creproprocod = ProgramaSerializer()
    class Meta:
        model = CredencialPrograma
        fields = [
            "creprocod",
            "creprofecemi",
            "creprofeccad",
            "creprocer",
            "creprodip",
            "creprocarnet",
            "creproestcod",
            "creproprocod",
        ]


class CertificadoCursoMatriculadoSerializerList(serializers.ModelSerializer):
    cercurmatcurcod = MatriculaCursoSerializerList()
    class Meta:
        model = CertificadoCursoMatriculado
        fields = [
            "cercurcod",
            "cercurcodcer",
            "cercurfecemi",
            "cercurfeccad",
            "cercurcarnet",
            "cercurmatcurcod",
        ]


class CertificadoCursoSerializerList(serializers.ModelSerializer):
    cercurestcod = UserSimpleSerializerList()
    cercurcurcod = CursoSerializerList()
    class Meta:
        model = CertificadoCurso
        fields = [
            "cercurcod",
            "cercurcodcer",
            "cercurfecemi",
            "cercurfeccad",
            "cercurcarnet",
            "cercurestcod",
            "cercurcurcod",
        ]


class CredencialProgramaMatriculadoSerializerListMin(serializers.ModelSerializer):
    crepromatprocod = MatriculaProgramaSerializerList()
    class Meta:
        model = CredencialProgramaMatriculado
        fields = [
            "creprofecemi",
            "creprofeccad",
            "creprocer",
            "creprodip",
            "crepromatprocod",
        ]


class CredencialProgramaSerializerListMin(serializers.ModelSerializer):
    creproprocod = ProgramaSerializer()
    class Meta:
        model = CredencialPrograma
        fields = [
            "creprofecemi",
            "creprofeccad",
            "creprocer",
            "creprodip",
            "creproprocod",
        ]


class CertificadoCursoMatriculadoSerializerListMin(serializers.ModelSerializer):
    cercurmatcurcod = MatriculaCursoSerializerList()
    class Meta:
        model = CertificadoCursoMatriculado
        fields = [
            "cercurfecemi",
            "cercurfeccad",
            "cercurmatcurcod",
        ]


class CertificadoCursoSerializerListMin(serializers.ModelSerializer):
    cercurcurcod = CursoSerializerList()
    class Meta:
        model = CertificadoCurso
        fields = [
            "cercurfecemi",
            "cercurfeccad",
            "cercurcurcod",
        ]