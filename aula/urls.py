from django.urls import path
from rest_framework.documentation import include_docs_urls
from .views.views_create import *
from .views.views_list import *
from .views.views_retrieve import *
from .views.views_update import *
from .views.views_destroy import *
from .views.views import *
from .views.views_upload import UploadPDFView


urlpatterns = [
    path('docs/', include_docs_urls(title="Aula API")),
    
    # Custom Views
    
    path('programa/<int:programa_id>/cursos/', CursosPorProgramaListAPIView.as_view(), name='cursos-por-programa'),
    path('curso/<int:curso_id>/modulos/', ModulosPorCursoListAPIView.as_view(), name='modulos-por-curso'),
    path('programa/<int:programa_id>/estudiante/<str:estudiante_id>/registrosexamenes/', RegistrosExamenesPorProgramaPorEstudianteListAPIView.as_view(), name='registros-de-examenes-por-programa-y-estudiante'),
    path('programa/<int:programa_id>/examenes/', ExamenesPorProgramaListAPIView.as_view(), name='examenes-por-programa'),
    path('guardar-respuestas-examen/', GuardarRespuestasExamenProgramaAPIView.as_view(), name='guardar_respuestas_examen'),
    
    path('generar-examen/', GenerarExamenView.as_view(), name='generar_examen'),
    path("modulo/<int:pk>/update-txt/", UpdateModuloTxtContentView.as_view(), name="update-txt"),
    
    # Vistas para pdf
    
    path('curso/<int:curso_id>/upload-pdf/', UploadPDFView.as_view(), name='upload_pdf'),
    path('curso/<int:curso_id>/pdf-pages/', GetPdfPagesView.as_view(), name='pdf-pages'),
    path('curso/<int:curso_id>/process-pdf/', ProcessPdfView.as_view(), name='process-pdf'),
    
    # Vistas de modulos txt
    
    path('modulos_txt/<int:curso_id>/', ModuloTxtContentView.as_view(), name='modulo_txt_content'),
    
    # List
    
    path('respuestas-examen-programa/<str:estudiante_email>/<int:programa_id>/<int:examen_id>/', RespuestaExamensProgramaListAPIView.as_view(), name='respuestas-examen-programa'),
    path('programas-matriculados/<str:estudiante_email>/', ProgramasMatriculadosPorEstudianteListAPIView.as_view(), name='programas-matriculados-list'),
    path('cursos-matriculados/<str:estudiante_email>/', CursosMatriculadosPorEstudianteListAPIView.as_view(), name='cursos_matriculados-list'),
    path('registros-examen-programa/<int:programa_id>/<int:estudiante_id>', RegistroExamenProgramaPorMatriculaListView.as_view(), name='registros-examen-programa-por-matricula-list'),
    path('registros-examen-curso/<str:estudiante_email>/', RegistroExamenCursoPorEstudianteListView.as_view(), name='registro-examen-curso-por-estudiante-list'),
    
    path('cursos-gratuitos/', CursosGratuitosListAPIView.as_view(), name='cursos-gratuitos-list'),
    path('programa/', ProgramaListAPIView.as_view(), name='programa-list'),
    path('curso/', CursoListAPIView.as_view(), name='curso-list'),
    path('modulo/', ModuloListAPIView.as_view(), name='modulo-list'),
    path('examen/', ExamenListAPIView.as_view(), name='examen-list'),
    path('pregunta/', PreguntaListAPIView.as_view(), name='pregunta-list'),
    path('alternativa/', AlternativaListAPIView.as_view(), name='alternativa-list'),
    
    # Create
    
    path('programa/create/', ProgramaCreateAPIView.as_view(), name='programa-create'),
    path('curso/create/', CursoCreateAPIView.as_view(), name='curso-create'),
    path('modulo/create/', ModuloCreateAPIView.as_view(), name='modulo-create'),
    path('examen/create/', ExamenCreateAPIView.as_view(), name='examen-create'),
    path('pregunta/create/', PreguntaCreateAPIView.as_view(), name='pregunta-create'),
    path('alternativa/create/', AlternativaCreateAPIView.as_view(), name='alternativa-create'),
    
    # Detail
    
    path('programa/<int:pk>/', ProgramaRetrieveAPIView.as_view(), name='programa-detail'),
    path('curso/<int:pk>/', CursoRetrieveAPIView.as_view(), name='curso-detail'),
    path('modulo/<int:pk>/', ModuloRetrieveAPIView.as_view(), name='modulo-detail'),
    path('examen/<int:pk>/', ExamenRetrieveAPIView.as_view(), name='examen-detail'),
    path('xexamen/<int:pk>/', XExamenRetrieveAPIView.as_view(), name='Xexamen-detail'),
    path('pregunta/<int:pk>/', PreguntaRetrieveAPIView.as_view(), name='pregunta-detail'),
    path('alternativa/<int:pk>/', AlternativaRetrieveAPIView.as_view(), name='alternativa-detail'),
    
    # Update
    
    path('programa/<int:pk>/update/', ProgramaUpdateAPIView.as_view(), name='programa-update'),
    path('curso/<int:pk>/update/', CursoUpdateAPIView.as_view(), name='curso-update'),
    path('modulo/<int:pk>/update/', ModuloUpdateAPIView.as_view(), name='modulo-update'),
    path('examen/<int:pk>/update/', ExamenUpdateAPIView.as_view(), name='examen-update'),
    path('pregunta/<int:pk>/update/', PreguntaUpdateAPIView.as_view(), name='pregunta-update'),
    path('alternativa/<int:pk>/update/', AlternativaUpdateAPIView.as_view(), name='alternativa-update'),
    
    # Delete
    
    path('programa/<int:pk>/delete/', ProgramaDestroyAPIView.as_view(), name='programa-delete'),
    path('curso/<int:pk>/delete/', CursoDestroyAPIView.as_view(), name='curso-delete'),
    path('modulo/<int:pk>/delete/', ModuloDestroyAPIView.as_view(), name='modulo-delete'),
    path('examen/<int:pk>/delete/', ExamenDestroyAPIView.as_view(), name='examen-delete'),
    path('pregunta/<int:pk>/delete/', PreguntaDestroyAPIView.as_view(), name='pregunta-delete'),
    path('alternativa/<int:pk>/delete/', AlternativaDestroyAPIView.as_view(), name='alternativa-delete'),
]
