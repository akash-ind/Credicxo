from django.shortcuts import render
from django.contrib.auth.models import User
from login.serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Create your views here.


def genMissingErros(dct, values):
    """
    function to dictionary for required values
    """
    errors = {}
    for value in values:
        if not dct.get(value):
            errors[value] = "required"
    return errors

@csrf_exempt
def createUser(request):
    """
    endpoint for creating Student, Teacher, admin 
    """
    required_values = ["first_name", "email", "last_name",
    "username", "type", "password"]
    errors = genMissingErros(request.POST, required_values)
    if errors:
        return JsonResponse(errors)
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    type = request.POST["type"]
    user = User(first_name=first_name,
                last_name=last_name, email = email, username = username)
    user.set_password(password)
    print(type)
    try:
        user.save()
    except Exception as e:
        return JsonResponse({"error": str(e)})
    return JsonResponse({"done":"user created successfully"})


def ret_user(request):
    user = request.user
    print(user)
    return JsonResponse({"user":user})