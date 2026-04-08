from django.contrib import admin
from .models import *

# Register your models here.

# Registro del modelo UserSimple personalizado
@admin.register(UserSimple)
class UserSimpleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'userdocide',
        'usernom',
        'userape',
        'userlic',
        'userpai',
        'userdep',
        'userpro',
        'userdis',
        'userdir',
    )
    search_fields = ('id', 'usernom', 'userape', 'userdocide',)
    list_filter = ('userdep',)


# Registro del modelo EStudiante usuario personalizado
@admin.register(EstudianteUser)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'is_staff',
        'is_active',
    )
    search_fields = ('email',)
    list_filter = ('is_staff',)
    autocomplete_fields = ['usuario']