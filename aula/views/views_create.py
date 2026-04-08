from rest_framework.generics import (
    CreateAPIView
)
from ..serializers import *
from ..models import *


class EstadoExamenCreateAPIView(CreateAPIView):
    queryset = EstadoExamen.objects.all()
    serializer_class = EstadoExamenSerializer


class ProgramaCreateAPIView(CreateAPIView):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer


class CursoCreateAPIView(CreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class ModuloCreateAPIView(CreateAPIView):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer


class ExamenCreateAPIView(CreateAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class PreguntaCreateAPIView(CreateAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class AlternativaCreateAPIView(CreateAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer

