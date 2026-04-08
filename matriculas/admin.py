from django.contrib import admin
from .models import MatriculaPrograma, MatriculaCurso

# Register your models here.


# Registro del modelo Matricula Programa
@admin.register(MatriculaPrograma)
class MatriculaProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'matproestcod',
        'matproter',
        'matpropun',
        'matprofecini',
        'matprofecfin',
        'matproprocod',
        'matproestregcod'
    )
    search_fields = ('matproestcod__usuario__usernom', 'matproestcod__usuario__userape', 'matproestcod__usuario__userdocide', 'matproprocod__procod','matproprocod__pronom')
    list_filter = ('matproprocod',)
    autocomplete_fields = ['matproestcod','matproprocod','matproestregcod']


# Registro del modelo Matricula Curso
@admin.register(MatriculaCurso)
class MatriculaCursoAdmin(admin.ModelAdmin):
    list_display = (
        'matcurcod',
        'matcurfecini',
        'matcurfecfin',
        'matcurestcod',
        'matcurcurcod',
        'matcurestregcod'
    )
    search_fields = ('matcurestcod__usuario__usernom', 'matcurestcod__usuario__userape', 'matcurestcod__usuario__userdocide', 'matcurcurcod__curcod','matcurcurcod__curnom')
    list_filter = ('matcurcurcod',)
    autocomplete_fields = ['matcurestcod','matcurcurcod','matcurestregcod']