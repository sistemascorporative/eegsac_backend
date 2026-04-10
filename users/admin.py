from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import EstudianteUserCreationForm, EstudianteUserChangeForm

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
class EstudianteAdmin(UserAdmin):
    add_form = EstudianteUserCreationForm
    form = EstudianteUserChangeForm

    model = EstudianteUser

    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'usuario')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'usuario', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(EstudianteUser, EstudianteAdmin)