from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.db.models import Max
import re

# Create your models here.

def generar_codigo_certificado(curso_id):
    # Obtener todos los códigos de ambos modelos para un curso
    codigos_curso = CertificadoCurso.objects.filter(cercurcurcod__curcod=curso_id).values_list("cercurcodcer", flat=True)
    codigos_matricula = CertificadoCursoMatriculado.objects.filter(cercurmatcurcod__matcurcurcod__curcod=curso_id).values_list("cercurcodcer", flat=True)
    # Unirlos en una lista
    todos_codigos = list(codigos_curso) + list(codigos_matricula)
    # Extraer solo la parte numérica antes del primer guion
    numeros = []
    for codigo in todos_codigos:
        match = re.match(r"(\d+)-", codigo)
        if match:
            numeros.append(int(match.group(1)))
    # Si no hay ningún código, empezamos desde 1
    if not numeros:
        nuevo_num = 100
    else:
        nuevo_num = max(numeros) + 1
    # Formatear con 4 dígitos
    nuevo_num_str = str(nuevo_num).zfill(4)
    # Año actual y sufijo fijo (puedes cambiarlo según tu lógica)
    from datetime import datetime
    anio = datetime.now().year
    sufijo = "SSG"
    # Construir el nuevo código
    nuevo_codigo = f"{nuevo_num_str}-{anio}-{sufijo}"
    return nuevo_codigo


class Empresa(models.Model):
    empcod = models.AutoField(verbose_name="Código", db_column='empcod', primary_key=True)
    empnom = models.CharField(verbose_name="Nombre corto", db_column='empnom', max_length=100, blank=False)
    empruc = models.CharField(verbose_name="RUC", db_column='empruc', max_length=11, unique=True, blank=True, null=True)
    emprazsoc = models.CharField(verbose_name="Razón Social", db_column='emprazsoc', max_length=255, blank=True, null=True)
    empinf = models.TextField( verbose_name="Dato extra", db_column='empinf', max_length=255, blank=True, null=True)
    empestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='empestregcod')
    empfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='empfeccre', auto_now_add=True)   # creado una vez
    empfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='empfecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'empresa'
        managed = True
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return f"{self.empnom} ({self.empruc})"

class CertificadoComplemento(models.Model):
    certcomcod = models.AutoField(verbose_name="Código", db_column='certcomcod', primary_key=True)
    certcomnom = models.CharField(verbose_name="Nombre", db_column='certcomnom', max_length=255, blank=False, null=False)
    certcomfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='certcomfeccre', auto_now_add=True)   # creado una vez
    certcomfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='certcomfecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'certificado_complemento'
        managed = True
        verbose_name = 'Certificado Complemento'
        verbose_name_plural = 'Certificados Complemento'
    
    def __str__(self):
        return f"{self.certcomnom}"


class CredencialProgramaMatriculado(models.Model):
    creprocod = models.AutoField(verbose_name="Código", db_column='creprocod', primary_key=True)
    creprofecemi = models.DateField(verbose_name="Fecha de emisión", db_column='creprofecemi', blank=False, null=False)
    creprofeccad = models.DateField(verbose_name="Fecha de caducidad", db_column='creprofeccad', blank=True, null=True)
    creprocer = models.BooleanField(verbose_name="Certificado", db_column='creprocer', blank=False, null=False, default=True, db_default=True)
    creprodip = models.BooleanField(verbose_name="Con diploma", db_column='creprodip', blank=False, null=False, default=True, db_default=True)
    creprocarnet = models.BooleanField(verbose_name="Con carnet", db_column='creprocarnet', blank=False, null=False, default=True, db_default=True)
    creproempcod = models.ForeignKey(Empresa, models.PROTECT, verbose_name="Código Empresa", db_column='creproempcod', blank=True, null=True)
    crepromatprocod = models.ForeignKey('matriculas.MatriculaPrograma', models.PROTECT, verbose_name="Código Matrícula Programa", db_column='crepromatprocod', blank=False, null=False)
    creprofeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='creprofeccre', auto_now_add=True)   # creado una vez
    creprofecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='creprofecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'credencial_programa_matriculado'
        managed = True
        verbose_name = 'Credencial para Programa Matriculado'
        verbose_name_plural = 'Credenciales para Programa Matriculado'
    
    def save(self, *args, **kwargs):
        if not self.creprofeccad:
            self.creprofeccad = (
                self.creprofecemi
                + relativedelta(years=5)
                - relativedelta(days=1)
            )
        super().save(*args, **kwargs)


class CredencialPrograma(models.Model):
    creprocod = models.AutoField(verbose_name="Código", db_column='creprocod', primary_key=True)
    creprofecemi = models.DateField(verbose_name="Fecha de emisión", db_column='creprofecemi', blank=False, null=False)
    creprofeccad = models.DateField(verbose_name="Fecha de caducidad", db_column='creprofeccad', blank=True, null=True)
    creprocer = models.BooleanField(verbose_name="Certificado", db_column='creprocer', blank=False, null=False, default=True, db_default=True)
    creprodip = models.BooleanField(verbose_name="Con diploma", db_column='creprodip', blank=False, null=False, default=True, db_default=True)
    creprocarnet = models.BooleanField(verbose_name="Con carnet", db_column='creprocarnet', blank=False, null=False, default=True, db_default=True)
    creproestcod = models.ForeignKey('users.UserSimple', models.PROTECT, verbose_name="Código Estudiante", db_column='creproestcod', blank=False, null=False)
    creproprocod = models.ForeignKey('aula.Programa', models.PROTECT, verbose_name="Código Programa", db_column='creproprocod', blank=False, null=False)
    creproempcod = models.ForeignKey(Empresa, models.PROTECT, verbose_name="Código Empresa", db_column='creproempcod', blank=True, null=True)
    creprofeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='creprofeccre', auto_now_add=True)   # creado una vez
    creprofecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='creprofecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'credencial_programa'
        managed = True
        verbose_name = 'Credencial para Programa'
        verbose_name_plural = 'Credenciales para Programa'
    
    def save(self, *args, **kwargs):
        if not self.creprofeccad:
            self.creprofeccad = (
                self.creprofecemi
                + relativedelta(years=5)
                - relativedelta(days=1)
            )
        super().save(*args, **kwargs)


class CertificadoCursoMatriculado(models.Model):
    cercurcod = models.AutoField(verbose_name="Código", db_column='cercurcod', primary_key=True)
    cercurcodcer = models.CharField(verbose_name="Código del certificado", db_column='cercurcodcer', max_length=13, blank=True)
    cercurfecemi = models.DateField(verbose_name="Fecha de emisión", db_column='cercurfecemi', blank=False, null=False)
    cercurfeccad = models.DateField(verbose_name="Fecha de caducidad", db_column='cercurfeccad', blank=True, null=True)
    cercurcarnet = models.BooleanField(verbose_name="Con carnet", db_column='cercurcarnet', blank=False, null=False, default=False, db_default=False)
    cercurempcod = models.ForeignKey(Empresa, models.PROTECT, verbose_name="Código Empresa", db_column='cercurempcod', blank=True, null=True)
    cercurmatcurcod = models.ForeignKey('matriculas.MatriculaCurso', models.PROTECT, verbose_name="Código Matrícula Curso", db_column='cercurmatcurcod', blank=False, null=False)
    cercurfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='cercurfeccre', auto_now_add=True)   # creado una vez
    cercurfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='cercurfecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'certificado_curso_matriculado'
        managed = True
        verbose_name = 'Certificado para Curso Matriculado'
        verbose_name_plural = 'Certificados para Curso Matriculado'
    
    def save(self, *args, **kwargs):
        if not self.cercurcodcer:
            self.cercurcodcer = generar_codigo_certificado(self.cercurmatcurcod.matcurcurcod_id)
        # Fecha de caducidad = 1 año - 1 día
        if not self.cercurfeccad:
            self.cercurfeccad = (
                self.cercurfecemi
                + relativedelta(years=1)
                - relativedelta(days=1)
            )
        super().save(*args, **kwargs)


class CertificadoCurso(models.Model):
    cercurcod = models.AutoField(verbose_name="Código", db_column='cercurcod', primary_key=True)
    cercurcodcer = models.CharField(verbose_name="Código del certificado", db_column='cercurcodcer', max_length=13, blank=True)
    cercurfecemi = models.DateField(verbose_name="Fecha de emisión", db_column='cercurfecemi', blank=False, null=False)
    cercurfeccad = models.DateField(verbose_name="Fecha de caducidad", db_column='cercurfeccad', blank=True, null=True)
    cercurfecreg = models.DateTimeField(verbose_name="Fecha de registro",db_column="cercurfecreg", auto_now_add=True)
    cercurcarnet = models.BooleanField(verbose_name="Con carnet", db_column='cercurcarnet', blank=False, null=False, default=False, db_default=False)
    cercurestcod = models.ForeignKey('users.UserSimple', models.PROTECT, verbose_name="Código Estudiante", db_column='cercurestcod', blank=False, null=False)
    cercurcurcod = models.ForeignKey('aula.Curso', models.PROTECT, verbose_name="Código Curso", db_column='cercurcurcod', blank=False, null=False)
    cercurempcod = models.ForeignKey(Empresa, models.PROTECT, verbose_name="Código Empresa", db_column='cercurempcod', blank=True, null=True)
    cercurcomcod = models.ForeignKey(CertificadoComplemento, models.PROTECT, verbose_name="Código complemento", db_column='cercurcomcod', blank=True, null=True)
    cercurfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='cercurfeccre', auto_now_add=True)   # creado una vez
    cercurfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='cercurfecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'certificado_curso'
        managed = True
        verbose_name = 'Certificado para Curso'
        verbose_name_plural = 'Certificados para Curso'

    def save(self, *args, **kwargs):
        if not self.cercurcodcer:
            self.cercurcodcer = generar_codigo_certificado(self.cercurcurcod_id)
        # Fecha de caducidad = 1 año - 1 día
        if not self.cercurfeccad:
            self.cercurfeccad = (
                self.cercurfecemi
                + relativedelta(years=1)
                - relativedelta(days=1)
            )
        super().save(*args, **kwargs)