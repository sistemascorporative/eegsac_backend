from django.db.models.signals import m2m_changed, post_save, post_delete, pre_save
from django.dispatch import receiver
from matriculas.models import MatriculaPrograma, MatriculaCurso
from .models import (
    Programa, Modulo, Examen, Pregunta
)
from .services.programa_service import recalcular_numero_cursos
from .services.curso_service import recalcular_numero_modulos
from .services.examen_service import recalcular_numero_preguntas
from .services.registro_examen_programa_service import (
    crear_registros_examen_por_programa,
    eliminar_registros_programa,
)
from aula.services.registro_examen_curso_service import (
    crear_registro_examen_curso,
    eliminar_registros_examen_curso,
)
from aula.utils.model_helpers import guardar_fk_anterior
import logging


# Configuración del logger
logger = logging.getLogger(__name__)


"""
Actualizar número de cursos en la tabla Programa
"""
@receiver(m2m_changed, sender=Programa.cursos.through)
def programa_cursos_changed(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
        recalcular_numero_cursos(instance)


"""
Actualiza el número de modulos en la tabla Curso
cuando se crea, actualiza o elimina un modulo
"""
@receiver(pre_save, sender=Modulo)
def modulo_pre_save(sender, instance, **kwargs):
    guardar_fk_anterior(
        instance=instance,
        model=Modulo,
        fk_field='modcurcod',
        attr_name='_curso_anterior'
    )

@receiver(post_save, sender=Modulo)
def modulo_post_save(sender, instance, **kwargs):
    recalcular_numero_modulos(instance.modcurcod)

    curso_anterior = getattr(instance, '_curso_anterior', None)
    if curso_anterior and curso_anterior != instance.modcurcod:
        recalcular_numero_modulos(curso_anterior)

@receiver(post_delete, sender=Modulo)
def modulo_post_delete(sender, instance, **kwargs):
    recalcular_numero_modulos(instance.modcurcod)


"""
Actualiza el número de preguntas de la tabla Examen
cuando se crea, actualiza o elimina una pregunta
"""
@receiver(pre_save, sender=Pregunta)
def pregunta_pre_save(sender, instance, **kwargs):
    guardar_fk_anterior(
        instance=instance,
        model=Pregunta,
        fk_field='preexacod',
        attr_name='_examen_anterior'
    )

@receiver(post_save, sender=Pregunta)
def pregunta_post_save(sender, instance, **kwargs):
    recalcular_numero_preguntas(instance.preexacod)

    examen_anterior = getattr(instance, '_examen_anterior', None)
    if examen_anterior and examen_anterior != instance.preexacod:
        recalcular_numero_preguntas(examen_anterior)

@receiver(post_delete, sender=Pregunta)
def pregunta_post_delete(sender, instance, **kwargs):
    recalcular_numero_preguntas(instance.preexacod)


"""
Signal para crear registros de exámenes para todos los cursos de un programa
cuando se realiza una matrícula para el programa.
"""
@receiver(post_save, sender=MatriculaPrograma)
def matricula_programa_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    crear_registros_examen_por_programa(
        programa=instance.matproprocod,
        estudiante=instance.matproestcod,
    )


"""
Signal para eliminar los registros de examen asociados a una matrícula de programa.
"""
@receiver(post_delete, sender=MatriculaPrograma)
def matricula_programa_post_delete(sender, instance, **kwargs):
    eliminar_registros_programa(
        programa=instance.matproprocod,
        estudiante=instance.matproestcod,
    )


"""
Signal para crear un registro de examen curso para una matrícula de curso
"""
@receiver(post_save, sender=MatriculaCurso)
def matricula_curso_post_save(sender, instance, created, **kwargs):
    if created:
        crear_registro_examen_curso(instance)


"""
Signal para eliminar los registros de examen asociados a una matrícula de curso.
"""
@receiver(post_delete, sender=MatriculaCurso)
def matricula_curso_post_delete(sender, instance, **kwargs):
    eliminar_registros_examen_curso(instance)