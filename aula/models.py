from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class EstadoExamen(models.Model):
    estexacod = models.AutoField(verbose_name="Código", db_column='estexacod', primary_key=True)
    estexanom = models.CharField(verbose_name="Nombre de Estado", db_column='estexanom', max_length=40, blank=False, unique=True)
    estexafeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='estexafeccre', auto_now_add=True)   # creado una vez
    estexafecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='estexafecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'estado_examen'
        managed = True
        verbose_name = 'EstadoExamen'
        verbose_name_plural = 'EstadosExamenes'

    def __str__(self):
        return self.estexanom


class Curso(models.Model):
    curcod = models.PositiveIntegerField(verbose_name="Código", db_column='curcod', primary_key=True)
    curnom = models.CharField(verbose_name="Nombre", db_column='curnom', max_length=100, blank=False)
    curnomeng = models.CharField(verbose_name="Nombre en Inglés", db_column='curnomeng', max_length=100, blank=False)
    curfre = models.BooleanField(verbose_name="Gratuito", db_column='curfre', default=False, db_default=False)
    curnummod = models.PositiveIntegerField( verbose_name="N° módulos", db_column='curnummod', default=0, db_default=0)
    cursrcpdf = models.FileField(verbose_name="Archivo PDF", db_column='cursrcpdf', upload_to='cursos_pdf/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    curdaylen = models.PositiveIntegerField(verbose_name="Días acumulados", db_column='curdaylen', default=0, db_default=0)
    curnumhor = models.PositiveIntegerField(verbose_name="N° horas", db_column='curnumhor', default=0, db_default=0)
    curestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='curestregcod')
    curfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='curfeccre', auto_now_add=True)   # creado una vez
    curfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='curfecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'curso'
        managed = True
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        return f"{self.curcod} - {self.curnom}"


class Programa(models.Model):
    procod = models.PositiveIntegerField(verbose_name="Código", db_column='procod', primary_key=True)
    pronom = models.CharField(verbose_name="Nombre de Grado", db_column='pronom',max_length=200, blank=False)
    pronomeng = models.CharField(verbose_name="Nombre de Grado en inglés", db_column='pronomeng',max_length=200, blank=True, default='', db_default='')
    prodip = models.CharField(verbose_name="Nombre de Diploma", db_column='prodip',max_length=200, blank=True, default='', db_default='')
    prodipeng = models.CharField(verbose_name="Nombre de Diploma en inglés", db_column='prodipeng',max_length=200, blank=True, default='', db_default='')
    procodosh = models.CharField(verbose_name="Código Abreviado", db_column='procodosh', max_length=30)
    pronumhor = models.PositiveIntegerField( verbose_name="N° horas", db_column='pronumhor', default=0, db_default=0)
    pronumcur = models.PositiveIntegerField( verbose_name="N° cursos", db_column='pronumcur', default=0, db_default=0)
    cursos = models.ManyToManyField(Curso, related_name='programas', verbose_name="Cursos", blank=True)
    proestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='proestregcod')
    profeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='profeccre', auto_now_add=True)   # creado una vez
    profecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='profecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'programa'
        managed = True
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
    
    def __str__(self):
        return f"{self.procod} - {self.pronom}"


class Modulo(models.Model):
    modcod = models.PositiveIntegerField(verbose_name="Código", db_column='modcod', primary_key=True)
    modnom = models.CharField(verbose_name="Nombre", db_column='modnom', max_length=100, blank=False)
    modsrctxt = models.FileField(verbose_name="Archivo TXT", db_column='modsrctxt', upload_to='modulo_pdf/', max_length=120, blank=True, null=True)
    modcurcod = models.ForeignKey(Curso, models.PROTECT, verbose_name="Código Curso", db_column='modcurcod')
    modestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='modestregcod')
    modfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='modfeccre', auto_now_add=True)   # creado una vez
    modfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='modfecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'modulo'
        managed = True
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
    
    def __str__(self):
        return f"{self.modcurcod} - {self.modnom}"


class Examen(models.Model):
    exacurcod = models.OneToOneField(Curso, models.PROTECT, verbose_name="Código Curso", db_column='exacurcod', primary_key=True)
    exanumpre = models.PositiveIntegerField( verbose_name="N° preguntas", db_column='exanumpre', default=0, db_default=0)
    exaestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='exaestregcod')
    exafeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='exafeccre', auto_now_add=True)   # creado una vez
    exafecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='exafecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'examen'
        managed = True
        verbose_name = 'Examen'
        verbose_name_plural = 'Examenes'
    
    def __str__(self):
        return f"{self.exacurcod.curnom}"


class Pregunta(models.Model):
    precod = models.PositiveIntegerField(verbose_name="Código", db_column='precod', primary_key=True)
    pretex = models.CharField(verbose_name="Texto",db_column="pretex", max_length=500)
    preexp = models.CharField(verbose_name="Explicación",db_column="preexp", max_length=1000, default='', db_default='')
    prenummod = models.IntegerField(verbose_name="N° modulo al que pertenece", db_column="prenummod", default=0, db_default=0)
    preexacod = models.ForeignKey(Examen, models.PROTECT, verbose_name="Código Examen", db_column='preexacod')
    preestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EStReg", db_column='preestregcod')
    prefeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='prefeccre', auto_now_add=True)   # creado una vez
    prefecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='prefecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'pregunta'
        managed = True
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
    
    def __str__(self):
        return f"{self.precod} - {self.pretex}"


class Alternativa(models.Model):
    altcod = models.PositiveIntegerField(verbose_name="Código", db_column='altcod', primary_key=True)
    alttex = models.CharField(verbose_name="Texto", db_column='alttex', max_length=500)
    altcor = models.BooleanField(verbose_name="Correcto", db_column='altcor')
    altprecod = models.ForeignKey(Pregunta, models.PROTECT, verbose_name="Código Pregunta", db_column='altprecod')
    altestregcod = models.ForeignKey('core.EstadoRegistro', models.PROTECT, verbose_name="Código EstReg", db_column='altestregcod')
    altfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='altfeccre', auto_now_add=True)   # creado una vez
    altfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='altfecupd', auto_now=True)   # actualizado siempre
    
    class Meta:
        db_table = 'alternativa'
        managed = True
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'
    
    def __str__(self):
        return self.alttex


class RespuestaExamenPrograma(models.Model):
    resprocod = models.AutoField(verbose_name="Código", db_column='resprocod', primary_key=True)
    respropun = models.DecimalField(verbose_name="Puntuación", db_column='respropun', max_digits=5, decimal_places=2)
    resproestcod = models.ForeignKey('users.EstudianteUser', models.PROTECT, verbose_name="Código Estudiante", db_column='resproestcod')
    resproprocod = models.ForeignKey(Programa, models.PROTECT, verbose_name="Código Programa", db_column='resproprocod')
    resproexacod = models.ForeignKey(Examen, on_delete=models.PROTECT, verbose_name="Código Examen", db_column='resproexacod')
    resproprecod = models.ForeignKey(Pregunta, on_delete=models.PROTECT, verbose_name="Pregunta", db_column='resproprecod')
    resproaltcod = models.ForeignKey(Alternativa, on_delete=models.PROTECT, verbose_name="Alternativa seleccionada", db_column='resproaltcod')
    resprofeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='resprofeccre', auto_now_add=True)   # creado una vez
    resprofecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='resprofecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'respuesta_examen_programa'
        managed = True
        verbose_name = 'Respuesta de Examen por Programa'
        verbose_name_plural = 'Respuestas de Exámenes por Programa'
        unique_together = ('resproestcod', 'resproprocod', 'resproexacod', 'resproprecod')

    def __str__(self):
        return f"{self.resproestcod.usuario.usernom} - {self.resproprecod} - {self.resproaltcod}"


class RespuestaExamenCurso(models.Model):
    rescurcod = models.AutoField(verbose_name="Código", db_column='rescurcod', primary_key=True)
    rescurpun = models.DecimalField(verbose_name="Puntuación", db_column='rescurpun', max_digits=5, decimal_places=2)
    rescurestcod = models.ForeignKey('users.EstudianteUser', models.PROTECT, verbose_name="Código Estudiante", db_column='rescurestcod')
    rescurexacod = models.ForeignKey(Examen, on_delete=models.PROTECT, verbose_name="Código Examen", db_column='rescurexacod')
    rescurprecod = models.ForeignKey(Pregunta, on_delete=models.PROTECT, verbose_name="Pregunta", db_column='rescurprecod')
    rescuraltcod = models.ForeignKey(Alternativa, on_delete=models.PROTECT, verbose_name="Alternativa seleccionada", db_column='rescuraltcod')
    rescurfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='rescurfeccre', auto_now_add=True)   # creado una vez
    rescurfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='rescurfecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'respuesta_examen_curso'
        managed = True
        verbose_name = 'Respuesta de Examen por Curso'
        verbose_name_plural = 'Respuestas de Exámenes por Curso'
        unique_together = ('rescurestcod', 'rescurexacod', 'rescurprecod')  # Una respuesta por pregunta en un intento.

    def __str__(self):
        return f"{self.rescurestcod.usuario.usernom} - {self.rescurprecod} - {self.rescuraltcod}"



class RegistroExamenPrograma(models.Model):
    regexaprocod = models.AutoField(verbose_name="Código", db_column='regexaprocod', primary_key=True)
    regexapropun = models.DecimalField(verbose_name="Puntuación", db_column='regexapropun', max_digits=5, decimal_places=2, default=0.00, db_default=0.00)
    regexaproint = models.PositiveIntegerField(verbose_name="N° intentos", db_column='regexaproint', default=0, db_default=0)
    regexaproprocod = models.ForeignKey(Programa, models.PROTECT, verbose_name="Matrícula del Programa", db_column='regexaproprocod')
    regexaproestcod = models.ForeignKey('users.EstudianteUser', models.PROTECT, verbose_name="Estudiante", db_column='regexaproestcod')
    regexaproexacod = models.ForeignKey(Examen, models.PROTECT, verbose_name="Código del Examen", db_column='regexaproexacod')
    regexaproestexacod = models.ForeignKey(EstadoExamen, models.PROTECT, verbose_name="Estado del Examen", db_column='regexaproestexacod')
    regexaprofeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='regexaprofeccre', auto_now_add=True)   # creado una vez
    regexaprofecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='regexaprofecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'registro_examen_programa'
        managed = True
        verbose_name = 'Registro de Examen por Programa'
        verbose_name_plural = 'Registros de Exámenes por Programa'
        unique_together = ('regexaproestcod', 'regexaproprocod', 'regexaproexacod')  # Una matrícula solo puede tener un registro por examen.

    def __str__(self):
        return f"{self.regexaproestcod.usuario.usernom} - {self.regexaproexacod} - {self.regexaproestexacod.estexanom}"


class RegistroExamenCurso(models.Model):
    regexacurcod = models.AutoField(verbose_name="Código", db_column='regexacurcod', primary_key=True)
    regexacurpun = models.DecimalField(verbose_name="Puntuación", db_column='regexacurpun', max_digits=5, decimal_places=2, default=0.00, db_default=0.00)
    regexacurint = models.PositiveIntegerField(verbose_name="N° intentos", db_column='regexacurint', default=0, db_default=0)
    regexacurcurcod = models.ForeignKey(Curso, models.PROTECT, verbose_name="Matrícula del Curso", db_column='regexacurcurcod')
    regexacurestcod = models.ForeignKey('users.EstudianteUser', models.PROTECT, verbose_name="Matrícula del Programa", db_column='regexacurestcod')
    regexacurexacod = models.ForeignKey(Examen, models.PROTECT, verbose_name="Código del Examen", db_column='regexacurexacod')
    regexacurestexacod = models.ForeignKey(EstadoExamen, models.PROTECT, verbose_name="Estado del Examen", db_column='regexacurestexacod')
    regexacurfeccre = models.DateTimeField(verbose_name="Fecha de creación", db_column='regexacurfeccre', auto_now_add=True)   # creado una vez
    regexacurfecupd = models.DateTimeField(verbose_name="Fecha de modificación", db_column='regexacurfecupd', auto_now=True)   # actualizado siempre

    class Meta:
        db_table = 'registro_examen_curso'
        managed = True
        verbose_name = 'Registro de Examen por Curso'
        verbose_name_plural = 'Registros de Exámenes por Curso'
        unique_together = ('regexacurestcod', 'regexacurcurcod', 'regexacurexacod')

    def __str__(self):
        return f"{self.regexacurestcod.usuario.usernom} - {self.regexacurexacod} - {self.regexacurestexacod.estexanom}"