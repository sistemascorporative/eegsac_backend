from django.db import models
from aula.models import Programa


# Create your models here.


class BrochurePrograma(models.Model):
    broprocod = models.AutoField(verbose_name="Código", db_column='broprocod', primary_key=True)
    broproprocod = models.ForeignKey('aula.Programa', models.PROTECT, verbose_name="Código Programa", db_column='broproprocod')
    bronummod = models.PositiveIntegerField(verbose_name="Número de módulos", db_column='bronummod', default=0, db_default=0)
    broestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='broestregcod')
    brofeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='brofeccre', auto_now_add=True)   # creado una vez
    brofecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='brofecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'brochure_programa'
        managed = True
        verbose_name = 'Brochure'
        verbose_name_plural = 'Brochures'
    
    def __str__(self):
        return self.broproprocod.pronom


class BModulo(models.Model):
    bmodcod = models.AutoField(verbose_name="Código", db_column='bmodcod', primary_key=True)
    bmodnomes = models.CharField(verbose_name="Nombre en español", db_column='bmodnomes', max_length=100, blank=False)
    bmodnomen = models.CharField(verbose_name="Nombre en Ingles", db_column='bmodnomen', max_length=100, blank=False)
    bmodbrocod = models.ForeignKey(BrochurePrograma, models.PROTECT, verbose_name="Código Brochure", db_column='bmodbrocod')
    bmodestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='bmodestregcod')
    bmodfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='bmodfeccre', auto_now_add=True)   # creado una vez
    bmodfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='bmodfecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'bmodulo'
        managed = True
        verbose_name = 'BModulo'
        verbose_name_plural = 'BModulos'
    
    def __str__(self):
        return self.bmodnomes
