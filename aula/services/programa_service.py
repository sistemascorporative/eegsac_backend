from django.db import transaction

def recalcular_numero_cursos(programa):
    def _update():
        programa.pronumcur = programa.cursos.count()
        programa.save(update_fields=['pronumcur'])

    transaction.on_commit(_update)