from django.db import models

# Create your models here.

class EstadoRegistro(models.Model):
  estregcod = models.AutoField(verbose_name="Código", db_column='estregcod', primary_key=True)
  estregnom = models.CharField(verbose_name="Nombre", db_column='estregnom', max_length=40, blank=False, unique=True)
  estregfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='estregfeccre', auto_now_add=True)   # creado una vez
  estregfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='estregfecupd', auto_now=True)   # actualizado siempre
  
  class Meta:
    db_table = 'estado_registro'
    managed = True
    verbose_name = 'EstadoRegistro'
    verbose_name_plural = 'EstadosRegistro'
  
  def __str__(self):
    return self.estregnom