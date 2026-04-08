from django.contrib import admin
from .models import *


@admin.register(BrochurePrograma)
class BrochureAdmin(admin.ModelAdmin):
    list_display = (
        'broprocod',
        'broproprocod',
        'bronummod',
    )


@admin.register(BModulo)
class BModuloAdmin(admin.ModelAdmin):
    list_display = (
        'bmodnomes',
        'bmodnomen',
        'bmodbrocod',
    )

