from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('token/access/', jwt_views.TokenObtainPairView.as_view(), name='token_access'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]