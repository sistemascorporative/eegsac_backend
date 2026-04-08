from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your models here.

class MatriculaPrograma(models.Model):
    matprocod = models.AutoField(verbose_name="Código", db_column='matprocod', primary_key=True)
    matprofecini = models.DateField(verbose_name="Fecha de inicio", db_column='matprofecini', blank=True, null=True)
    matprofecfin = models.DateField(verbose_name="Fecha de finalización", db_column='matprofecfin', blank=True, null=True)
    matproter = models.BooleanField(verbose_name="Finalizado", db_column='matproter', blank=False, null=False, default=False, db_default=False)
    matpropun = models.DecimalField(verbose_name="Puntuación", db_column='matpropun', max_digits=5, decimal_places=2, default=0.00, db_default=0.00, blank=True, null=True)
    matpropor = models.DecimalField(verbose_name="Porcentaje de avance", db_column='matpropor', max_digits=5, decimal_places=2, default=0.00, db_default=0.00, blank=True, null=True)
    matproestcod = models.ForeignKey('users.EstudianteUser', models.PROTECT, verbose_name="Código Estudiante", db_column='matproestcod')
    matproprocod = models.ForeignKey('aula.Programa', models.PROTECT, verbose_name="Código Programa", db_column='matproprocod')
    matproestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='matproestregcod')
    matprofeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='matprofeccre', auto_now_add=True)   # creado una vez
    matprofecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='matprofecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'matricula_programa'
        managed = True
        verbose_name = 'Matricula para Programa'
        verbose_name_plural = 'Matricula para Programas'
        unique_together = ('matproestcod','matproprocod')

    def clean(self):
        """
        Regla de negocio: No se permite cambiar el programa de una matrícula existente.
        """
        if not self.pk:
            return  # Es una matrícula nueva - permitido
        original = MatriculaPrograma.objects.only(
            'matproestcod_id',
            'matproprocod_id'
        ).get(pk=self.pk)
        errores = {}
        if original.matproestcod_id != self.matproestcod_id:
            errores['matproestcod'] = 'No se puede cambiar el estudiante de una matrícula.'
        if original.matproprocod_id != self.matproprocod_id:
            errores['matproprocod'] = 'No se puede cambiar el programa de una matrícula.'
        if errores:
            raise ValidationError(errores)
    
    def save(self, *args, **kwargs):
        # Validaciones de negocio
        self.full_clean() # obliga a pasar por clean()
        if not self.matprofecini:
            self.matprofecini = date.today()
        if not self.matprofecfin and self.matprofecini:
            self.matprofecfin = self.matprofecini + relativedelta(months=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matproestcod.usuario.usernom} - {self.matproprocod.pronom}"


class MatriculaCurso(models.Model):
    matcurcod = models.AutoField(verbose_name="Código", db_column='matcurcod', primary_key=True)
    matcurfecini = models.DateField(verbose_name="Fecha de inicio", db_column='matcurfecini', blank=True, null=True)
    matcurfecfin = models.DateField(verbose_name="Fecha de finalización", db_column='matcurfecfin', blank=True, null=True)
    matcurter = models.BooleanField(verbose_name="Curso terminado", db_column='matcurter', blank=False, null=False, default=False, db_default=False)
    matcurestcod = models.ForeignKey('users.EstudianteUser', models.PROTECT, verbose_name="Código Estudiante", db_column='matcurestcod')
    matcurcurcod = models.ForeignKey('aula.Curso', models.PROTECT, verbose_name="Código Curso", db_column='matcurcurcod')
    matcurestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='matcurestregcod')
    matcurfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='matcurfeccre', auto_now_add=True)   # creado una vez
    matcurfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='matcurfecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'matricula_curso'
        managed = True
        verbose_name = 'Matricula para Curso'
        verbose_name_plural = 'Matricula para Cursos'
        unique_together = ('matcurestcod','matcurcurcod')

    def clean(self):
        if not self.pk:
            return
        original = MatriculaCurso.objects.only(
            'matcurestcod_id',
            'matcurcurcod_id'
        ).get(pk=self.pk)
        errores = {}
        if original.matcurestcod_id != self.matcurestcod_id:
            errores['matcurestcod'] = 'No se puede cambiar el estudiante de una matrícula.'
        if original.matcurcurcod_id != self.matcurcurcod_id:
            errores['matcurcurcod'] = 'No se puede cambiar el curso de una matrícula.'
        if errores:
            raise ValidationError(errores)

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.matcurfecini:
            self.matcurfecini = date.today()
        if not self.matcurfecfin and self.matcurfecini:
            self.matcurfecfin = self.matcurfecini + relativedelta(months=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matcurestcod.usuario.usernom} - {self.matcurcurcod.curnom}"
