from rest_framework import serializers
from aula.serializers import ProgramaSerializer
from aula. serializers_list_retrieve import CursoSerializerList
from .models import MatriculaPrograma, MatriculaCurso
from users.serializers_list_retrieve import EstudianteUserSerializerList

# Define los serializers para cada modelo

class MatriculaProgramaSerializerList(serializers.ModelSerializer):
    matproprocod = ProgramaSerializer()
    matproestcod = EstudianteUserSerializerList()
    class Meta:
        model = MatriculaPrograma
        fields = [
            "matprocod",
            "matproprocod",
            "matproestcod",
        ]


class MatriculaCursoSerializerList(serializers.ModelSerializer):
    matcurcurcod = CursoSerializerList()
    matcurestcod = EstudianteUserSerializerList()
    class Meta:
        model = MatriculaCurso
        fields = [
            "matcurcod",
            "matcurcurcod",
            "matcurestcod",
        ]