from django.contrib import admin
from .models import *


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'empcod',
        'empnom',
        'empruc',
        'emprazsoc',
        'empinf',
    )
    search_fields = ('emprazsoc','empruc')


@admin.register(CertificadoComplemento)
class CertificadoComplementoAdmin(admin.ModelAdmin):
    list_display = (
        'certcomcod',
        'certcomnom',
        'certcomfecupd',
    )
    search_fields = ('certcomnom',)


@admin.register(CredencialProgramaMatriculado)
class CredencialProgramaMatriculaAdmin(admin.ModelAdmin):
    list_display = (
        'crepromatprocod',
        'creprofecemi',
        'creprofeccad',
        'creprocer',
        'creprodip',
        'creprocarnet',
        'creproempcod',
    )
    search_fields = ('crepromatprocod__matproestcod__usuario__usernom', 'crepromatprocod__matproestcod__usuario__userape', 'crepromatprocod__matproestcod__usuario__userdocide', 'crepromatprocod__matproprocod__procod', 'crepromatprocod__matproprocod__pronom')
    list_filter = ('creproempcod',)
    autocomplete_fields = ['crepromatprocod','creproempcod']


@admin.register(CredencialPrograma)
class CredencialProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'creprocod',
        'creproestcod',
        'creproprocod',
        'creprofecemi',
        'creprofeccad',
        'creprocer',
        'creprodip',
        'creprocarnet',
        'creproempcod',
    )
    search_fields = ('creproestcod__usernom', 'creproestcod__userape', 'creproestcod__userdocide', 'creproprocod__procod', 'creproprocod__pronom',)
    list_filter = ('creproempcod',)
    autocomplete_fields = ['creproestcod','creproprocod','creproempcod']



# Registro del modelo CertificadoCursoMatricula
@admin.register(CertificadoCursoMatriculado)
class CertificadoCursoMatriculaAdmin(admin.ModelAdmin):
    list_display = (
        'cercurcodcer',
        'cercurmatcurcod',
        'cercurfecemi',
        'cercurfeccad',
        'cercurcarnet',
        'cercurempcod',
    )
    search_fields = ('cercurmatcurcod__matcurestcod__usuario__usernom', 'cercurmatcurcod__matcurestcod__usuario__userape', 'cercurmatcurcod__matcurestcod__usuario__userdocide',)
    list_filter = ('cercurempcod',)
    autocomplete_fields = ['cercurmatcurcod','cercurempcod']


# Registro del modelo CertificadoCurso
@admin.register(CertificadoCurso)
class CertificadoCursoAdmin(admin.ModelAdmin):
    list_display = (
        'cercurcodcer',
        'cercurestcod',
        'cercurcurcod',
        'cercurfecemi',
        'cercurfeccad',
        'cercurcarnet',
        'cercurempcod',
    )
    search_fields = ('cercurestcod__usernom', 'cercurestcod__userape', 'cercurestcod__userdocide', 'cercurcurcod__curcod', 'cercurcurcod__curnom',)
    list_filter = ('cercurempcod',)
    autocomplete_fields = ['cercurestcod','cercurcurcod','cercurempcod']