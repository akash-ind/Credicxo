from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #path('create/user/', views.createUser, name="create-student"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("check/user/", views.ret_user, name = "user"),
    path("list/users", views.ListUsers.as_view(), name="list_users"),
    path("create/user", views.CreateUser.as_view(), name="create_user"),
]
