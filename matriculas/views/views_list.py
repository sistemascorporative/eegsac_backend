from rest_framework.generics import (
    ListAPIView
)
from ..serializers_list_retrieve import *
from django.shortcuts import get_object_or_404
from users.models import EstudianteUser
from matriculas.models import MatriculaPrograma, MatriculaCurso

#ListAPIViews

"""
Endpoint para obtener las matrículas de programas según el correo del estudiante.
"""
class MatriculaProgramaPorEstudianteListView(ListAPIView):
    serializer_class = MatriculaProgramaSerializerList

    def get_queryset(self):
        email = self.kwargs.get('estudiante_email')
        estudiante = get_object_or_404(EstudianteUser, email=email)
        return MatriculaPrograma.objects.filter(matproestcod=estudiante)


"""
Endpoint para obtener las matrículas de cursos según el correo del estudiante.
"""
class MatriculaCursoPorEstudianteListView(ListAPIView):
    serializer_class = MatriculaCursoSerializerList

    def get_queryset(self):
        email = self.kwargs.get('estudiante_email')
        estudiante = get_object_or_404(EstudianteUser, email=email)
        return MatriculaCurso.objects.filter(matcurestcod=estudiante)