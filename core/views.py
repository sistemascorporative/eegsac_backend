from rest_framework.viewsets import ModelViewSet
from core.models import EstadoRegistro
from core.serializers import EstadoRegistroSerializer
from core.serializers_list_retrieve import EstadoRegistroSerializerList

# Create your views here.

class EstadoRegistroViewSet(ModelViewSet):
    """
    ViewSet para gestionar Estados de Registro.
    - list / retrieve → serializer de lectura
    - create / update / destroy → serializer de escritura
    """

    queryset = EstadoRegistro.objects.all().order_by("estregcod")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EstadoRegistroSerializerList
        return EstadoRegistroSerializer