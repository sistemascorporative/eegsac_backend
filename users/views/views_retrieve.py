from django.http import Http404
from rest_framework.generics import (
    RetrieveAPIView
)
from ..serializers_list_retrieve import *
from ..serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound


class EstudianteUserRetrieveAPIView(RetrieveAPIView):
    queryset = EstudianteUser.objects.all()
    serializer_class = EstudianteUserSerializerList


class UserSimpleRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = UserSimple.objects.all()
    serializer_class = UserSimpleSerializerList
    lookup_field = 'userdocide'
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="La persona con ese documento no está registrada en el sistema.")