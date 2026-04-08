from django.db import transaction

def recalcular_numero_preguntas(examen):
    def _update():
        examen.exanumpre = examen.pregunta_set.count()
        examen.save(update_fields=['exanumpre'])

    transaction.on_commit(_update)
