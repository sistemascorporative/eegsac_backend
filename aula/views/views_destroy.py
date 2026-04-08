from rest_framework.generics import (
    RetrieveDestroyAPIView
)
from ..serializers import *


class EstadoExamenDestroyAPIView(RetrieveDestroyAPIView):
    queryset = EstadoExamen.objects.all()
    serializer_class = EstadoExamenSerializer


class ProgramaDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer


class CursoDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class ModuloDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer


class ExamenDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class PreguntaDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class AlternativaDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer



