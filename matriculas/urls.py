from django.urls import path
from .views.views_create import *
from .views.views_list import *
from .views.views import *


urlpatterns = [
    
    # List
    
    path('matriculas-programa/<str:estudiante_email>/', MatriculaProgramaPorEstudianteListView.as_view(), name='matriculas-programa-por-estudiante-list'),
    
    # Create
    
    path('matricula-curso/create/', MatriculaCursoCreateAPIView.as_view(), name='matricula-curso-create'),
]