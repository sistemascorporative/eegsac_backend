from rest_framework.generics import (
    CreateAPIView
)
from ..serializers import MatriculaCursoSerializer
from ..models import MatriculaCurso, MatriculaPrograma



class MatriculaCursoCreateAPIView(CreateAPIView):
    queryset = MatriculaCurso.objects.all()
    serializer_class = MatriculaCursoSerializer