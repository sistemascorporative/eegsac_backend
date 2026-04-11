from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        user.save()#user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields["is_staff"] = True  # Forzar que is_staff sea True
        extra_fields["is_superuser"] = True  # Forzar que is_superuser sea True
        return self.create_user(email, password, **extra_fields)


class UserSimple(models.Model):
    """Usuarios básicos sin necesidad de email ni contraseña."""
    
    usernom = models.CharField(verbose_name="Nombre", db_column='usernom', max_length=60, blank=False)
    userape = models.CharField(verbose_name="Apellidos", db_column='userape', max_length=60, blank=False)
    userdocide = models.CharField(verbose_name="Documento de identidad", db_column='userdocide', max_length=50, blank=False, unique=True)
    userlic = models.CharField(verbose_name="Licencia", db_column='userlic', max_length=10, blank=True, null=True)
    userpai = models.CharField(verbose_name="Pais", db_column='userpai', max_length=50, blank=True, null=True, default='')
    userdep = models.CharField(verbose_name="Departamento", db_column='userdep', max_length=50, blank=True, null=True, default='')
    userpro = models.CharField(verbose_name="Provincia", db_column='userpro', max_length=50, blank=True, null=True, default='')
    userdis = models.CharField(verbose_name="Distrito", db_column='userdis', max_length=50, blank=True, null=True, default='')
    userdir = models.CharField(verbose_name="Dirección", db_column='userdir', max_length=100, blank=True, null=True, default='')
    userestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='userestregcod')
    userfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='userfeccre', auto_now_add=True)   # creado una vez
    userfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='userfecupd', auto_now=True)   # actualizado siempre
    
    def convertir_a_usuario(self, email, password):
        """Convierte esta instancia de UserSimple en un usuario que puede iniciar sesión."""
        if hasattr(self, 'estudianteuser'):
            raise ValueError("Este usuario ya tiene una cuenta de acceso.")
        # Crear el usuario con acceso a la plataforma
        usuario = EstudianteUser.objects.create_user(
            usuario=self,  # Usa el UserSimple como PK
            email=email,
            password=password
        )
        return usuario
    
    def __str__(self):
        return f"{self.userdocide} - {self.usernom} {self.userape}"


class EstudianteUser(AbstractBaseUser, PermissionsMixin):
    """Usuarios que pueden iniciar sesión en la plataforma."""

    usuario = models.OneToOneField(
        UserSimple, on_delete=models.CASCADE, verbose_name="Usuario", db_column='user', unique=True, null=False
    )
    email = models.CharField(verbose_name="Usuario", db_column='email', unique=True, max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usuario']
    
    def get_full_name(self):
        return self.usuario.usernom + "" + self.usuario.userape
    
    def get_name(self):
        return self.usuario.usernom
    
    def __str__(self):
        return f"{self.email}"