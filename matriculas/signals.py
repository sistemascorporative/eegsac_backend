from django.db.models.signals import post_save
from django.db.models import Avg, Count
from decimal import Decimal, ROUND_HALF_UP
from django.dispatch import receiver
from aula.models import RespuestaExamenPrograma, RegistroExamenCurso
from .models import MatriculaPrograma

#singals

"""
Actualizar si ha finalizado un curso
"""
#@receiver(post_save, sender=RespuestaExamenCurso)
#def update_matricula_curso(sender, instance, **kwargs):
    
    

"""
Actualizar el promedio de matricula de un programa, actualizar porcentaje de avance de un programa y si ha finalizado el programa
"""
@receiver(post_save, sender=RespuestaExamenPrograma)
def update_matricula_programa(sender, instance, **kwargs):
    estudiante = instance.resproestcod
    programa = instance.resproprocod

    # Obtener todas las respuestas del estudiante en ese programa
    respuestas = RespuestaExamenPrograma.objects.filter(
        resproestcod=estudiante,
        resproprocod=programa
    )

    # Calcular el promedio de puntajes (ignorando los nulos)
    promedio = respuestas.aggregate(promedio=Avg('respropun'))['promedio'] or 0.00
    promedio_decimal = Decimal(promedio).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Número de respuestas del estudiante en el programa
    num_respuestas = respuestas.count()

    # Número de cursos en el programa
    num_cursos = programa.cursos.count()

    # Calcular porcentaje de avance
    porcentaje = 0.00
    if num_cursos > 0:
        porcentaje = (Decimal(num_respuestas) / Decimal(num_cursos)) * Decimal(100)
        porcentaje = porcentaje.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Obtener la matrícula del programa
    try:
        matricula = MatriculaPrograma.objects.get(
            matproestcod=estudiante,
            matproprocod=programa
        )

        # Actualizar el promedio y el porcentaje de avance
        matricula.matpropun = promedio_decimal
        matricula.matpropor = porcentaje

        # Verificar si el estudiante ha terminado el programa
        if promedio_decimal >= Decimal("70.00") and num_respuestas == num_cursos:
            matricula.matproter = True

        matricula.save()

    except MatriculaPrograma.DoesNotExist:
        pass