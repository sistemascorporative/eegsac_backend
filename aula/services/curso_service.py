from django.db import transaction

def recalcular_numero_modulos(curso):
    def _update():
        curso.curnummod = curso.modulo_set.count()
        curso.save(update_fields=['curnummod'])

    transaction.on_commit(_update)
