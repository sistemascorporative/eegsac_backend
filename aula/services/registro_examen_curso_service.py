import logging
from django.db import transaction
from aula.models import Examen, EstadoExamen, RegistroExamenCurso

logger = logging.getLogger(__name__)


@transaction.atomic
def crear_registro_examen_curso(matricula):
    """
    Crea el registro de examen_curso cuando se crea una matrícula de curso.
    """
    curso = matricula.matcurcurcod

    try:
        examen = Examen.objects.get(exacurcod=curso)
    except Examen.DoesNotExist:
        logger.warning(
            f"[RegistroExamenCurso] Curso sin examen asociado: {curso.curcod}"
        )
        return

    estado_pendiente, _ = EstadoExamen.objects.get_or_create(
        estexanom="Pendiente"
    )

    RegistroExamenCurso.objects.get_or_create(
        regexacurcurcod=curso,
        regexacurestcod=matricula.matcurestcod,
        regexacurexacod=examen,
        defaults={
            "regexacurpun": 0.00,
            "regexacurint": 0,
            "regexacurestexacod": estado_pendiente,
        }
    )


@transaction.atomic
def eliminar_registros_examen_curso(matricula):
    """
    Elimina los registros asociados cuando se elimina la matrícula.
    """
    registros = RegistroExamenCurso.objects.filter(
        regexacurcurcod=matricula.matcurcurcod,
        regexacurestcod=matricula.matcurestcod
    )

    cantidad, _ = registros.delete()

    logger.info(
        f"[RegistroExamenCurso] {cantidad} registros eliminados "
        f"(Estudiante {matricula.matcurestcod.id}, "
        f"Curso {matricula.matcurcurcod.curcod})"
    )