from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import Curso
import os


class UploadPDFView(APIView):
    def post(self, request, curso_id):
        try:
            # Obtener el curso correspondiente
            curso = Curso.objects.get(curcod=curso_id)
            
            # Verificar si se ha enviado un archivo
            if 'cursrcpdf' not in request.FILES:
                return Response({'error': 'No se envió ningún archivo PDF.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener el archivo PDF
            pdf_file = request.FILES['cursrcpdf']
            
            # Verificar si ya existe un archivo PDF y eliminarlo
            if curso.cursrcpdf:
                # Verifica que el archivo exista y luego elimínalo
                if os.path.isfile(curso.cursrcpdf.path):
                    os.remove(curso.cursrcpdf.path)

            # Asignar el archivo al campo cursrcpdf del modelo
            curso.cursrcpdf = pdf_file
            curso.save()

            return Response({'message': 'PDF cargado exitosamente.'}, status=status.HTTP_200_OK)
        
        except Curso.DoesNotExist:
            return Response({'error': 'Curso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
