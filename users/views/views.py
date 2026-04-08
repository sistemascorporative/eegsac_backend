from rest_framework.permissions import AllowAny
from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import EstudianteUser
from ..serializers_list_retrieve import EstudianteUserSerializerList
from ..serializers import EstudianteUserSerializer

# Create your views here.

class PublicUserViewSet(UserViewSet):
    permission_classes = [AllowAny]


class EstudianteUserByEmailAPIView(APIView):
    def get(self, request, email):
        estudiante = get_object_or_404(EstudianteUser, email=email)
        serializer = EstudianteUserSerializerList(estudiante)
        return Response(serializer.data, status=status.HTTP_200_OK)