from rest_framework.generics import (
    RetrieveUpdateAPIView
)
from ..serializers import *

# UpdateAPIView

class EstadoExamenUpdateAPIView(RetrieveUpdateAPIView):
    queryset = EstadoExamen.objects.all()
    serializer_class = EstadoExamenSerializer


class ProgramaUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer


class CursoUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class ModuloUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer


class ExamenUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class PreguntaUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class AlternativaUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer


