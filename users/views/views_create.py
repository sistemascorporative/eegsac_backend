from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from ..models import UserSimple, EstudianteUser
from ..serializers import RegisterUserSerializer


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user_simple, created = UserSimple.objects.get_or_create(
                        userdocide=serializer.validated_data['userdocide'],
                        defaults={
                            'usernom': serializer.validated_data['usernom'],
                            'userape': serializer.validated_data['userape'],
                            'userlic': serializer.validated_data.get('userlic', ''),
                            'userpai': serializer.validated_data.get('userpai', ''),
                            'userdep': serializer.validated_data.get('userdep', ''),
                            'userpro': serializer.validated_data.get('userpro', ''),
                            'userdis': serializer.validated_data.get('userdis', ''),
                            'userdir': serializer.validated_data.get('userdir', '')
                        }
                    )
                    
                    if hasattr(user_simple, 'estudianteuser'):
                        return Response({"error": "Este usuario ya tiene una cuenta de acceso."}, status=status.HTTP_400_BAD_REQUEST)
                    
                    estudiante_user = EstudianteUser.objects.create(
                        usuario=user_simple,
                        email=serializer.validated_data['email'],
                        is_active=False
                    )
                    estudiante_user.set_password(serializer.validated_data['password'])
                    estudiante_user.save()
                    
                return Response({"message": "Usuario registrado exitosamente. Esperando activación."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
