from django.contrib import admin
from .models import *

# Register your models here.

# Registro del modelo Estado de Examen
@admin.register(EstadoExamen)
class EstadoExamenAdmin(admin.ModelAdmin):
    list_display = (
        'estexacod',
        'estexanom',
        'estexafeccre',
        'estexafecupd'
    )
    search_fields = ('estexanom',)


# Registro del modelo Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'curcod',
        'curnom',
        'curnummod',
        'curfre',
        'curdaylen',
        'curestregcod'
    )
    search_fields = ('curcod', 'curnom')
    list_filter = ('curfre', 'curestregcod')
    ordering = ('curcod',)
    autocomplete_fields = ['curestregcod']


# Registro del modelo Programa
@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'procod',
        'pronom',
        'procodosh',
        'pronumcur',
        'pronumhor',
        'proestregcod'
    )
    search_fields = ('procod','pronom','procodosh')
    filter_horizontal = ('cursos',)
    list_filter = ('proestregcod',)
    ordering = ('procod',)
    autocomplete_fields = ['proestregcod']


# Registro del modelo Modulo
@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = (
        'modcod',
        'modnom',
        'modcurcod',
        'modestregcod'
    )
    search_fields = ('modcod','modnom',)
    list_filter =    ('modcurcod','modestregcod',)
    autocomplete_fields = ['modcurcod', 'modestregcod']


# Registro del modelo Examen
@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = (
        'exacurcod',
        'exanumpre',
        'exaestregcod',
    )
    search_fields = ('exacurcod__curcod','exacurcod__curnom')
    list_filter = ('exaestregcod',)
    autocomplete_fields = ['exacurcod', 'exaestregcod']


# Registro del modelo Pregunta
@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = (
        'precod',
        'pretex',
        'preexacod',
        'preestregcod',
    )
    search_fields = ('precod','pretex','preexacod__exacurcod__curcod','preexacod__exacurcod__curnom')
    list_filter = ('preestregcod','preexacod')
    autocomplete_fields = ['preexacod', 'preestregcod']


# Registro del modelo Alternativa
@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    list_display = (
        'altcod',
        'altcor',
        'alttex',
        'altprecod',
        'altestregcod',
    )
    search_fields = ('alttex', 'altcod')
    list_filter = ('altestregcod',)
    autocomplete_fields = ['altprecod', 'altestregcod']


# Registro del modelo RespuestaExamenPrograma
@admin.register(RespuestaExamenPrograma)
class RespuestaExamenProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'resprocod',
        'respropun',
        'resproestcod',
        'resproprocod',
        'resproexacod',
        'resproprecod',
        'resproaltcod',
    )
    search_fields = ('resproestcod__usuario__userdocide','resproprocod__procod','resproexacod__exacurcod__curcod','resproprecod__pretex',)
    list_filter = ('resproexacod',)
    autocomplete_fields = ['resproestcod', 'resproprocod', 'resproexacod', 'resproprecod', 'resproaltcod']


# Registro del modelo RespuestaExamenCurso
@admin.register(RespuestaExamenCurso)
class RespuestaExamenCursoAdmin(admin.ModelAdmin):
    list_display = (
        'rescurcod',
        'rescurpun',
        'rescurestcod',
        'rescurexacod',
        'rescurprecod',
        'rescuraltcod',
    )
    search_fields = ('rescurestcod__usuario__userdocide','rescurexacod__exacurcod__curcod','rescurprecod__pretex',)
    list_filter = ('rescurexacod',)
    autocomplete_fields = ['rescurestcod', 'rescurexacod', 'rescurprecod', 'rescuraltcod']


@admin.register(RegistroExamenPrograma)
class RegistroExamenProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'regexaprocod',
        'regexapropun',
        'regexaproint',
        'regexaproprocod',
        'regexaproestcod',
        'regexaproexacod',
        'regexaproestexacod',
    )
    search_fields = ('regexaproprocod__procod','regexaproprocod__pronom','regexaproestcod__usuario__userdocide','regexaproexacod__exacurcod__curcod',)
    list_filter = ('regexaproprocod',)
    autocomplete_fields = ['regexaproestcod', 'regexaproprocod', 'regexaproexacod', 'regexaproestexacod']


@admin.register(RegistroExamenCurso)
class RegistroExamenCursoAdmin(admin.ModelAdmin):
    list_display = (
        'regexacurcod',
        'regexacurpun',
        'regexacurint',
        'regexacurcurcod',
        'regexacurestcod',
        'regexacurexacod',
        'regexacurestexacod',
    )
    search_fields = ('regexacurcurcod__curcod','regexacurcurcod__curnom','regexacurestcod__usuario__userdocide','regexacurestcod__usuario__usernom', 'regexacurestcod__usuario__userape')
    list_filter = ('regexacurcurcod',)
    autocomplete_fields = ['regexacurcurcod', 'regexacurestcod', 'regexacurexacod', 'regexacurestexacod']