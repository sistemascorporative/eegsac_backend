from rest_framework import serializers
from .serializers import ProgramaSerializer
from .models import *
from users.serializers_list_retrieve import EstudianteUserSerializerList
from core.serializers_list_retrieve import EstadoRegistroSerializerList

# Define los serializers para cada modelo

class EstadoExamenSerializerList(serializers.ModelSerializer):
    class Meta:
        model = EstadoExamen
        fields = [
            "estexacod",
            "estexanom"
        ]


class ProgramaSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = [
            "procod",
            "procodosh",
            "pronom",
        ]


class CursoSerializerList(serializers.ModelSerializer):
    #curprocod = ProgramaSerializerList()
    curestregcod = EstadoRegistroSerializerList()
    class Meta:
        model = Curso
        fields = [
            "curcod",
            "curnom",
            "curnomeng",
            "curnummod",
            "curfre",
            "curestregcod"
        ]


class ModuloSerializerList(serializers.ModelSerializer):
    modcurcod = CursoSerializerList()
    modestregcod = EstadoRegistroSerializerList()
    class Meta:
        model = Modulo
        fields = [
            "modcod",
            "modnom",
            "modcurcod",
            "modestregcod"
        ]


class ExamenSerializerList(serializers.ModelSerializer):
    exacurcod = CursoSerializerList()
    exaestregcod = EstadoRegistroSerializerList()
    class Meta:
        model = Examen
        fields = [
            "exacurcod",
            "exaestregcod"
        ]


class PreguntaSerializerList(serializers.ModelSerializer):
    preexacod = ExamenSerializerList()
    preestregcod = EstadoRegistroSerializerList()
    class Meta:
        model = Pregunta
        fields = [
            "precod",
            "pretex",
            "preexacod",
            "preestregcod"
        ]


class AlternativaSerializerList(serializers.ModelSerializer):
    altprecod = PreguntaSerializerList()
    altestregcod = EstadoRegistroSerializerList()
    class Meta:
        model = Alternativa
        fields = [
            "altcod",
            "alttex",
            "altcor",
            "altprecod",
            "altestregcod"
        ]


class RespuestaExamenProgramaSerializerList(serializers.ModelSerializer):
    resproexacod = ExamenSerializerList()
    resproprecod = PreguntaSerializerList()
    resproaltcod = AlternativaSerializerList()
    class Meta:
        model = RespuestaExamenPrograma
        fields = [
            "resprocod",
            "respropun",
            "resproestcod",
            "resproprocod",
            "resproexacod",
            "resproprecod",
            "resproaltcod",
        ]


class RespuestaExamenCursoSerializerList(serializers.ModelSerializer):
    resestcod = EstudianteUserSerializerList()
    resexacod = ExamenSerializerList()
    resprecod = PreguntaSerializerList()
    resaltcod = AlternativaSerializerList()
    class Meta:
        model = RespuestaExamenCurso
        fields = [
            "rescurcod",
            "rescurpun",
            "rescurestcod",
            "rescurexacod",
            "rescurprecod",
            "rescuraltcod",
        ]


class RegistroExamenProgramaSerializerList(serializers.ModelSerializer):
    regexaproprocod = ProgramaSerializer()
    regexaproestcod = EstudianteUserSerializerList()
    regexaproexacod = ExamenSerializerList()
    regexaproestexacod = EstadoExamenSerializerList()
    class Meta:
        model = RegistroExamenPrograma
        fields = [
            "regexaprocod",
            "regexapropun",
            "regexaproint",
            "regexaproprocod",
            "regexaproestcod",
            "regexaproexacod",
            "regexaproestexacod"
        ]


class RegistroExamenCursoSerializerList(serializers.ModelSerializer):
    regexacurcurcod = CursoSerializerList()
    regexacurestcod = EstudianteUserSerializerList()
    regexacurexacod = ExamenSerializerList()
    regexacurestexacod = EstadoExamenSerializerList()
    class Meta:
        model = RegistroExamenCurso
        fields = [
            "regexacurcod",
            "regexacurpun",
            "regexacurint",
            "regexacurcurcod",
            "regexacurestcod",
            "regexacurexacod",
            "regexacurestexacod"
        ]


class XAlternativaSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = [
            "altcod",
            "alttex",
            "altcor",
            "altprecod",
            "altestregcod"
        ]


class XPreguntaSerializerList(serializers.ModelSerializer):
    alternativas = XAlternativaSerializerList(many=True, source='alternativa_set')
    
    class Meta:
        model = Pregunta
        fields = [
            "precod",
            "pretex",
            "preexp",
            "preexacod",
            "preestregcod",
            "alternativas"
        ]


class XExamenSerializerList(serializers.ModelSerializer):
    preguntas = XPreguntaSerializerList(many=True, source='pregunta_set')
    exacurcod = CursoSerializerList()
    exaestregcod = EstadoRegistroSerializerList()
    
    class Meta:
        model = Examen
        fields = [
            "exacurcod",
            "exaestregcod",
            "preguntas"
        ]