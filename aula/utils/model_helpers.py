def guardar_fk_anterior(instance, model, fk_field, attr_name):
    """
    Guarda el valor anterior de una ForeignKey antes del save
    para detectar cambios de relación.
    """
    if not instance.pk:
        setattr(instance, attr_name, None)
        return

    try:
        anterior = model.objects.only(fk_field).get(pk=instance.pk)
        setattr(instance, attr_name, getattr(anterior, fk_field))
    except model.DoesNotExist:
        setattr(instance, attr_name, None)
