from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from authentication import views

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.test_end_point, name='test'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('request_password_reset/', views.request_password_reset, name='request-password-reset'),
    path('', views.get_routes),
]
