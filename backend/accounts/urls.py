from django.urls import path
from .views import StudentRegistrationView,StudentLoginView,StudentProfileView,MyRegistrationsView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('login/',StudentLoginView.as_view(),name='student-login'),
    path('profile/',StudentProfileView.as_view(),name='student-profile'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('my-registrations/',MyRegistrationsView.as_view(),name='my-registrations'),
]