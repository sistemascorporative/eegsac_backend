from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.views import PublicUserViewSet, EstudianteUserByEmailAPIView
from .views.views_retrieve import EstudianteUserRetrieveAPIView, UserSimpleRetrieveAPIView
from .views.views_create import RegisterUserView


urlpatterns = [
    path('usuario/register/', RegisterUserView.as_view(), name='register'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
    # Detail
    
    path('estudiante/<str:email>/', EstudianteUserByEmailAPIView.as_view(), name='estudiante-detail'),
    path('usersimple/<str:userdocide>/', UserSimpleRetrieveAPIView.as_view(), name='user-datail-docid'),
]