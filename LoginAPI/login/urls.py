from django.urls import path
from . import views


urlpatterns = [
    path('create/user/', views.createStudent, name="create-student"),
]
