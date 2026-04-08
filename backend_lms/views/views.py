from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


class ContactAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        name = request.data.get('name')
        lastname = request.data.get('lastname')
        email = request.data.get('email')
        phone = request.data.get('phone')
        course = request.data.get('course')
        address = request.data.get('address')
        information = request.data.get('information')

        try:
            send_mail(
                subject=f"SOLICITUD DE INFORMACIÓN DE {name} {lastname}",
                message=(
                    f"Nombres: {name}\n"
                    f"Apellidos: {lastname}\n"
                    f"Email: {email}\n"
                    f"Teléfono: {phone}\n"
                    f"Curso: {course}\n"
                    f"Dirección: {address}\n"
                    f"Mensaje:\n{information}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["administracion@eegsac.com"],
                fail_silently=False,
            )
            return Response({'detail': 'Correo enviado'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClaimsComplaintsApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        nombres = request.data.get('nombres')
        apellidos = request.data.get('apellidos')
        documento = request.data.get('documento')
        celular = request.data.get('celular')
        email = request.data.get('email')
        departamento = request.data.get('departamento')
        provincia = request.data.get('provincia')
        distrito = request.data.get('distrito')
        direccion = request.data.get('direccion')
        motivo = request.data.get('motivo')
        relacion = request.data.get('relacion')
        detalle = request.data.get('detalle')

        try:
            send_mail(
                subject=f"RECLAMACIÓN O QUEJA DE {nombres} {apellidos}",
                message=(
                    f"Nombres: {nombres}\n"
                    f"Apellidos: {apellidos}\n"
                    f"Documento o RUC: {documento}\n"
                    f"Celular: {celular}\n"
                    f"Email: {email}\n"
                    f"Departamento: {departamento}\n"
                    f"Provincia: {provincia}\n"
                    f"Distrito: {distrito}\n"
                    f"Direccion: {direccion}\n"
                    f"Motivo:\n{motivo}"
                    f"Relacion:\n{relacion}"
                    f"Detalle:\n{detalle}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["administracion@eegsac.com"],
                fail_silently=False,
            )
            return Response({'detail': 'Correo enviado'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)