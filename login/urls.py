from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("list/users", views.ListUsers.as_view(), name="list_users"),
    path("create/user", views.CreateUser.as_view(), name="create_user"),
    path("forgot-password", views.ForgotPassword.as_view(), name = "forgot-password"),
    path("change-password", views.ChangePassword.as_view(), name = "change-password")
]
