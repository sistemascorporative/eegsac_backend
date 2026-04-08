from rest_framework.routers import DefaultRouter
from core.views import EstadoRegistroViewSet


router = DefaultRouter()
router.register(r'estado-registro', EstadoRegistroViewSet, basename='estado-registro')


"""
GET         /estado-registro/	    List
POST	    /estado-registro/	    Create
GET	        /estado-registro/{id}/	Retrieve
PUT/PATCH	/estado-registro/{id}/	Update
DELETE	    /estado-registro/{id}/	Delete
"""


"""
urlpatterns = [
    # List
    path('estado-registro/', EstadoRegistroListAPIView.as_view(), name='estado-regitro-list'),
    # Create
    path('estado-registro/create/', EstadoRegistroCreateAPIView.as_view(), name='estado-registro-create'),
    # Detail
    path('estado-registro/<int:pk>/', EstadoRegistroRetrieveAPIView.as_view(), name='estado-registro-detail'),
    # Update
    path('estado-registro/<int:pk>/update/', EstadoRegistroUpdateAPIView.as_view(), name='estado-registro-update'),
    # Delete
    path('estado-registro/<int:pk>/delete/', EstadoRegistroDestroyAPIView.as_view(), name='estado-registro-delete'),
]
"""