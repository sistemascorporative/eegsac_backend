from rest_framework.generics import (
    ListAPIView
)
from ..serializers_list_retrieve import *
from ..serializers import *
from ..models import Curso, Programa
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from users.models import EstudianteUser

#ListAPIViews

class RespuestaExamensProgramaListAPIView(ListAPIView):
    serializer_class = RespuestaExamenProgramaSerializer

    def get_queryset(self):
            estudiante_email = self.kwargs.get('estudiante_email')
            programa_id = self.kwargs.get('programa_id')
            examen_id = self.kwargs.get('examen_id')
            if not estudiante_email:
                return RespuestaExamenPrograma.objects.none()
            # Filtrar programas directamente mediante la relación en MatriculaPrograma
            return RespuestaExamenPrograma.objects.filter(
                resproestcod__email=estudiante_email,
                resproprocod__procod=programa_id,
                resproexacod__exacurcod=examen_id
            )


class RespuestaExamensProgramaCursoListAPIView(ListAPIView):
    serializer_class = RespuestaExamenCursoSerializer

    def get_queryset(self):
            estudiante_email = self.kwargs.get('estudiante_email')
            examen_id = self.kwargs.get('examen_id')
            if not estudiante_email:
                return RespuestaExamenCurso.objects.none()
            # Filtrar programas directamente mediante la relación en MatriculaPrograma
            return RespuestaExamenCurso.objects.filter(
                rescurestcod__email=estudiante_email,
                rescurexacod__exacurcod=examen_id
            )


# Devuelve todos los programas matriculados de X estudiante
class ProgramasMatriculadosPorEstudianteListAPIView(ListAPIView):
    serializer_class = ProgramaSerializer
    
    def get_queryset(self):
        estudiante_email = self.kwargs.get('estudiante_email')
        if not estudiante_email:
            return Programa.objects.none()
        # Filtrar programas directamente mediante la relación en MatriculaPrograma
        return Programa.objects.filter(matriculaprograma__matproestcod__email=estudiante_email)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Manejar el caso en el que no se encuentra el email del estudiante
        if not queryset.exists() and not EstudianteUser.objects.filter(email=self.kwargs.get('estudiante_email')).exists():
            return Response(
                {"detail": "El estudiante con el email proporcionado no existe."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Devuelve todos los cursos matriculados de X estudiante
class CursosMatriculadosPorEstudianteListAPIView(ListAPIView):
    serializer_class = CursoSerializerList

    def get_queryset(self):
        estudiante_email = self.kwargs['estudiante_email']
        return Curso.objects.filter(matriculacurso__matcurestcod__email=estudiante_email)


# Devuelve todos los cursos gratuitos
class CursosGratuitosListAPIView(ListAPIView):
    queryset = Curso.objects.filter(curfre=True)
    serializer_class = CursoSerializerList



# Devuelve todos los cursos por X programa
class CursosPorProgramaListAPIView(ListAPIView):
    serializer_class = CursoSerializer

    def get_queryset(self):
        procod = self.kwargs.get('programa_id')
        if procod is not None:
            try:
                programa = Programa.objects.get(procod=procod)
                return programa.cursos.all()
            except Programa.DoesNotExist:
                return None  # Cambiado a None para diferenciar cuando el programa no existe
        return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:  # Si el programa no existe
            return Response({"detail": "Programa no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        if not queryset.exists():  # Si el programa existe pero no tiene cursos
            return Response({"detail": "No hay cursos en este programa."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Devuelve todos los módulos por X curso
class ModulosPorCursoListAPIView(ListAPIView):
    serializer_class = ModuloSerializer

    def get_queryset(self):
        curcod = self.kwargs.get('curso_id')        
        if curcod is not None:
            try:
                modulo = Modulo.objects.filter(modcurcod__curcod=curcod)
                print(modulo)
                return modulo
            except Modulo.DoesNotExist:
                return Modulo.objects.none()
        else:       
            return Modulo.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"detail": "Modulos not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
Endpoint para obtener los registros de exámenes de programa.
"""
class RegistroExamenProgramaPorMatriculaListView(ListAPIView):
    serializer_class = RegistroExamenProgramaSerializerList

    def get_queryset(self):
        procod = self.kwargs.get('programa_id')
        usercod = self.kwargs.get('estudiante_id')
        return RegistroExamenPrograma.objects.filter(regexaproprocod=procod, regexaproestcod=usercod)


"""
Endpoint para obtener todos los registros de exámenes de cursos de un estudiante.
"""
class RegistroExamenCursoPorEstudianteListView(ListAPIView):
    serializer_class = RegistroExamenCursoSerializerList

    def get_queryset(self):
        email = self.kwargs.get('estudiante_email')
        estudiante = get_object_or_404(EstudianteUser, email=email)
        #matriculas_curso = MatriculaCurso.objects.filter(matcurestcod=estudiante)
        return RegistroExamenCurso.objects.filter(regexacurestcod=estudiante)



# Devuelve todos los registros de examenes de X programa y X estudiante
class RegistrosExamenesPorProgramaPorEstudianteListAPIView(ListAPIView):
    serializer_class = RegistroExamenProgramaSerializerList
    
    def get_queryset(self):
        programa_id = self.kwargs.get('programa_id')
        estudiante_id = self.kwargs.get('estudiante_id')
        print(f"Programa ID: {programa_id}, Estudiante ID: {estudiante_id}")
        
        if programa_id is not None and estudiante_id is not None:
            try:
                # Obtener el programa por su ID
                programa = Programa.objects.get(procod=programa_id)
                
                # Obtener el estudiante por su ID
                estudiante = EstudianteUser.objects.get(email=estudiante_id)
                
                # Obtener los registros de examen asociados al programa y al estudiante
                registros_examen = RegistroExamenPrograma.objects.filter(
                    regexaproprocod=programa,  # Filtrar por programa
                    regexaproestcod=estudiante    # Filtrar por estudiante
                )
                return registros_examen
            
            except Programa.DoesNotExist:
                return RegistroExamenPrograma.objects.none()
            
            except EstudianteUser.DoesNotExist:
                return RegistroExamenPrograma.objects.none()
            
        else:
            return RegistroExamenPrograma.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"detail": "No se encontraron registros de exámenes para este programa y estudiante."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Devuelve todos los examenes de X programa
class ExamenesPorProgramaListAPIView(ListAPIView):
    serializer_class = ExamenSerializer
    
    def get_queryset(self):
        programa_id = self.kwargs.get('programa_id')
        if programa_id is not None:
            try:
                programa = Programa.objects.get(procod=programa_id)
                cursos = programa.cursos.all()
                examenes = Examen.objects.filter(exacurcod__in=cursos)
                return examenes
            except Programa.DoesNotExist:
                return Examen.objects.none()
        else:
            return Examen.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"detail": "No se encontraron exámenes para este programa."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProgramaListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Programa.objects.all()
    serializer_class = ProgramaSerializerList


class CursoListAPIView(ListAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializerList


class ModuloListAPIView(ListAPIView):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializerList


class ExamenListAPIView(ListAPIView):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializerList


class PreguntaListAPIView(ListAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializerList


class AlternativaListAPIView(ListAPIView):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializerList




