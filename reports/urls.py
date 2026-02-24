from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_reports, name="my_reports"),
    path("<int:pk>/download/", views.download_report, name="download_report"),
]
