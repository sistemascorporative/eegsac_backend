import logging
from django.db import transaction
from aula.models import Examen, EstadoExamen, RegistroExamenPrograma

logger = logging.getLogger(__name__)


@transaction.atomic
def crear_registros_examen_por_programa(programa, estudiante):
    """
    Crea los registros de examen para todos los cursos del programa
    al matricular un estudiante.
    """
    estado_pendiente, _ = EstadoExamen.objects.get_or_create(
        estexanom="Pendiente"
    )

    cursos = programa.cursos.select_related().all()

    for curso in cursos:
        try:
            examen = Examen.objects.get(exacurcod=curso)

            RegistroExamenPrograma.objects.get_or_create(
                regexaproprocod=programa,
                regexaproestcod=estudiante,
                regexaproexacod=examen,
                defaults={
                    "regexapropun": 0.00,
                    "regexaproint": 0,
                    "regexaproestexacod": estado_pendiente,
                },
            )

        except Examen.DoesNotExist:
            logger.warning(
                f"[RegistroExamenPrograma] Curso sin examen: {curso.curnom}"
            )


@transaction.atomic
def eliminar_registros_programa(programa, estudiante):
    """
    Elimina los registros de examen asociados a una matrícula de programa.
    """
    registros = RegistroExamenPrograma.objects.filter(
        regexaproprocod=programa,
        regexaproestcod=estudiante,
    )

    cantidad, _ = registros.delete()

    logger.info(
        f"[RegistroExamenPrograma] {cantidad} registros eliminados "
        f"(Estudiante {estudiante.id}, Programa {programa.procod})"
    )