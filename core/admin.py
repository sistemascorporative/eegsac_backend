from django.contrib import admin
from core.models import EstadoRegistro

# Register your models here.

# Registro del modelo Estado de Registro
@admin.register(EstadoRegistro)
class EstadoRegistroAdmin(admin.ModelAdmin):
    list_display = (
        'estregcod',
        'estregnom',
        'estregfecupd'
    )
    search_fields = ('estregnom',)