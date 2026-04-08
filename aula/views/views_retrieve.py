from rest_framework.generics import (
    RetrieveAPIView
)
from ..serializers_list_retrieve import *
from ..serializers import *

# RetrieveAPIVIew

class EstadoExamenRetrieveAPIView(RetrieveAPIView):
    queryset = EstadoExamen.objects.all()
    serializer_class = EstadoExamenSerializerList


class ProgramaRetrieveAPIView(RetrieveAPIView):
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializer


class CursoRetrieveAPIView(RetrieveAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializerList


class ModuloRetrieveAPIView(RetrieveAPIView):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializerList


class ExamenRetrieveAPIView(RetrieveAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializerList


class XExamenRetrieveAPIView(RetrieveAPIView):
    queryset = Examen.objects.all()
    serializer_class = XExamenSerializerList


class PreguntaRetrieveAPIView(RetrieveAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializerList


class AlternativaRetrieveAPIView(RetrieveAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializerList


