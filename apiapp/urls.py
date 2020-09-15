from django.urls import path

from apiapp import views

urlpatterns = [
    path("users/", views.EmployeeAPIView.as_view()),
    path("users/<str:id>/", views.EmployeeAPIView.as_view()),
]
