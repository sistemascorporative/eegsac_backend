from django.urls import path
from .views.views_list import *


urlpatterns = [
    
    # List
    path('credenciales/<str:docide>/', CredencialesPersonaAPIView.as_view(), name='credenciales-user'),

    path('credenciales/programa/matriculado/by-id/<int:pk>/', CredencialProgramaMatriculadoByPkListView.as_view(), name='credencial-programa-matriculado'),
    path('credenciales/programa/by-id/<int:pk>/', CredencialProgramaByPkListView.as_view(), name='credencial-programa'),
    path('certificados/curso/matriculado/by-id/<int:pk>/', CertificadoCursoMatriculadoByPkListView.as_view(), name='certificado-curso-matriculado'),
    path('certificados/curso/by-id/<int:pk>/', CertificadoCursoByPkListView.as_view(), name='certificado-curso'),

    path('credenciales/programa/matriculado/by-email/<str:estudiante_email>/', CredencialProgramaMatriculadoByEmailListView.as_view(), name='credencial-programa-by-email'),
    path('credenciales/programa/by-email/<str:estudiante_email>/', CredencialProgramaByEmailListView.as_view(), name='credencial-programa-by-email'),
    path('certificados/curso/matriculado/by-email/<str:estudiante_email>/', CertificadoCursoMatriculadoByEmailListView.as_view(), name='certificado-curso-matriculado-by-email'),
    path('certificados/curso/by-email/<str:estudiante_email>/', CertificadoCursoByEmailListView.as_view(), name='certificado-curso-by-email'),
    
    # List Obtener credenciales por documento de identidad
    
    path('credenciales/programa/matriculado/by-doc-identidad/<str:documento_identidad>/', CredencialProgramaMatriculadoByDocIdListView.as_view(), name='credencial-programa-by-documento-identidad'),
    path('credenciales/programa/by-doc-identidad/<str:documento_identidad>/', CredencialProgramaByDocIdListView.as_view(), name='credencial-programa-by-documento-identidad'),
    path('certificados/curso/matriculado/by-doc-identidad/<str:documento_identidad>/', CertificadoCursoMatriculadoByDocIdListView.as_view(), name='certificado-curso-matriculado-by-documento-identidad'),
    path('certificados/curso/by-doc-identidad/<str:documento_identidad>/', CertificadoCursoByDocIdListView.as_view(), name='certificado-curso-by-documento-identidad'),
]
