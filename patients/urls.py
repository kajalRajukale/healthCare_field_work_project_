from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='patient_register'),
    path('login/', views.patient_login, name='patient_login'),
    path('logout/', views.patient_logout, name='patient_logout'),
    path('dashboard/', views.dashboard, name='patient_dashboard'),
    path('profile/', views.profile, name='patient_profile'),
]
